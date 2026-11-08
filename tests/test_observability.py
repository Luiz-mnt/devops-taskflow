import json

from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families

from app.main import create_app


def samples_from(text, sample_name):
    return [
        sample
        for family in text_string_to_metric_families(text)
        for sample in family.samples
        if sample.name == sample_name
    ]


def test_metrics_exposes_counter_and_duration_with_normalized_routes(client):
    first = client.post("/tasks", json={"title": "Primeira"}).json()
    second = client.post("/tasks", json={"title": "Segunda"}).json()
    for task in (first, second):
        client.patch(f"/tasks/{task['id']}", json={"status": "completed"})

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    requests = samples_from(response.text, "taskflow_http_requests_total")
    completed = [sample for sample in requests if sample.labels["method"] == "PATCH"]
    assert len(completed) == 1
    assert completed[0].labels == {
        "method": "PATCH",
        "route": "/tasks/{task_id}",
        "status_code": "200",
    }
    assert completed[0].value == 2
    durations = samples_from(
        response.text, "taskflow_http_request_duration_seconds_count"
    )
    assert any(
        s.labels["route"] == "/tasks/{task_id}" and s.value == 2 for s in durations
    )
    assert 'route="/tasks/1"' not in response.text
    assert 'route="/tasks/2"' not in response.text


def test_unknown_paths_share_one_metric_label(client):
    assert client.get("/not-found/123456").status_code == 404
    assert client.get("/different/789012").status_code == 404

    text = client.get("/metrics").text
    requests = samples_from(text, "taskflow_http_requests_total")
    unmatched = [s for s in requests if s.labels["route"] == "unmatched"]
    assert len(unmatched) == 1
    assert unmatched[0].value == 2
    assert "123456" not in text
    assert "789012" not in text


def test_registries_are_isolated_between_application_instances(tmp_path):
    with TestClient(create_app(tmp_path / "first.db")) as first:
        first.get("/health")
        assert 'route="/health"' in first.get("/metrics").text

    with TestClient(create_app(tmp_path / "second.db")) as second:
        assert 'route="/health"' not in second.get("/metrics").text


def test_request_logs_are_json_without_sensitive_request_data(client, capsys):
    client.post(
        "/tasks?token=secret-query-value",
        json={"title": "private-task-title"},
        headers={"Authorization": "Bearer secret-header-value"},
    )
    client.patch("/tasks/123456", json={"status": "completed"})

    output = capsys.readouterr().out
    records = [json.loads(line) for line in output.splitlines()]
    assert len(records) == 2
    assert records[0]["event"] == "http_request"
    assert records[0]["status_code"] == 201
    assert records[1]["route"] == "/tasks/{task_id}"
    assert records[1]["status_code"] == 404
    assert all(record["duration_seconds"] >= 0 for record in records)
    for secret in ("secret-query-value", "private-task-title", "secret-header-value"):
        assert secret not in output
    assert "123456" not in output


def test_unhandled_failure_is_counted_without_logging_exception(
    tmp_path, monkeypatch, capsys
):
    application = create_app(tmp_path / "failure.db")

    def unavailable():
        raise RuntimeError("private-internal-detail")

    monkeypatch.setattr(application.state.store, "list_all", unavailable)
    with TestClient(application, raise_server_exceptions=False) as client:
        assert client.get("/tasks").status_code == 500
        metrics = client.get("/metrics").text

    failures = [
        sample
        for sample in samples_from(metrics, "taskflow_http_requests_total")
        if sample.labels["status_code"] == "500"
    ]
    assert len(failures) == 1
    assert failures[0].labels["route"] == "/tasks"
    assert failures[0].value == 1
    assert "private-internal-detail" not in capsys.readouterr().out


def test_nonstandard_methods_use_one_bounded_label(client):
    assert client.request("UNUSUAL", "/tasks").status_code == 405
    metrics = client.get("/metrics").text
    assert 'method="OTHER"' in metrics
    assert "UNUSUAL" not in metrics
