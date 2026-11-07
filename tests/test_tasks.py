import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def test_create_task_normalizes_title_and_defaults_to_pending(client):
    response = client.post("/tasks", json={"title": "  Estudar DevOps  "})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Estudar DevOps", "status": "pending"}


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": ""},
        {"title": "   \t\n"},
        {"title": "x" * 201},
        {"title": None},
        {"title": 123},
        {"title": "ok", "status": "completed"},
        [],
        {"title": "\x00"},
        {"title": "\x00abc"},
        {"title": "a\x00bc"},
    ],
    ids=[
        "missing",
        "empty",
        "whitespace",
        "too-long",
        "null",
        "number",
        "extra",
        "list",
        "null-character",
        "initial-null-character",
        "embedded-null-character",
    ],
)
def test_invalid_task_is_rejected_without_persistence(client, payload):
    assert client.post("/tasks", json=payload).status_code == 422
    assert client.get("/tasks").json() == []


def test_maximum_title_length_is_accepted(client):
    response = client.post("/tasks", json={"title": "x" * 200})
    assert response.status_code == 201
    assert len(response.json()["title"]) == 200


def test_list_tasks_returns_creation_order(client):
    assert client.get("/tasks").json() == []
    first = client.post("/tasks", json={"title": "Planejar"}).json()
    second = client.post("/tasks", json={"title": "Implementar"}).json()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_complete_task_is_persisted_and_idempotent(client):
    created = client.post("/tasks", json={"title": "Executar testes"}).json()
    endpoint = f"/tasks/{created['id']}"

    response = client.patch(endpoint, json={"status": "completed"})

    expected = {**created, "status": "completed"}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.patch(endpoint, json={"status": "completed"}).json() == expected
    assert client.get("/tasks").json() == [expected]


@pytest.mark.parametrize("task_id", [0, -1, "invalid", 9223372036854775808])
def test_invalid_task_id_is_rejected(client, task_id):
    response = client.patch(f"/tasks/{task_id}", json={"status": "completed"})
    assert response.status_code == 422


def test_missing_task_returns_404(client):
    response = client.patch("/tasks/999999", json={"status": "completed"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


@pytest.mark.parametrize(
    "payload", [{}, {"status": "pending"}, {"status": "done"}, {"status": None}]
)
def test_invalid_completion_does_not_change_task(client, payload):
    created = client.post("/tasks", json={"title": "Manter pendente"}).json()

    assert client.patch(f"/tasks/{created['id']}", json=payload).status_code == 422
    assert client.get("/tasks").json() == [created]


def test_title_is_treated_as_data_not_sql(client):
    title = "'); DROP TABLE tasks; --"
    assert client.post("/tasks", json={"title": title}).status_code == 201
    assert client.get("/tasks").json()[0]["title"] == title
    assert client.get("/health").status_code == 200


def test_persistence_between_application_instances(tmp_path):
    database_path = tmp_path / "nested" / "tasks.db"
    with TestClient(create_app(database_path)) as first_client:
        created = first_client.post("/tasks", json={"title": "Persistir"}).json()
        first_client.patch(f"/tasks/{created['id']}", json={"status": "completed"})

    with TestClient(create_app(database_path)) as second_client:
        assert second_client.get("/tasks").json() == [
            {**created, "status": "completed"}
        ]
        second = second_client.post("/tasks", json={"title": "Nova tarefa"}).json()
        assert second["id"] > created["id"]


def test_separate_databases_do_not_share_tasks(tmp_path):
    with TestClient(create_app(tmp_path / "first.db")) as first_client:
        first_client.post("/tasks", json={"title": "Somente primeiro banco"})

    with TestClient(create_app(tmp_path / "second.db")) as second_client:
        assert second_client.get("/tasks").json() == []
