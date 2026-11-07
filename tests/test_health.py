import sqlite3

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_checks_database(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "ok"}


def test_health_reports_corrupted_database_as_unavailable(tmp_path):
    database_path = tmp_path / "health.db"
    with TestClient(create_app(database_path)) as client:
        database_path.write_bytes(b"not a sqlite database")

        response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "unhealthy", "database": "unavailable"}
    assert str(database_path) not in response.text


def test_health_detects_missing_schema(tmp_path):
    database_path = tmp_path / "schema.db"
    with TestClient(create_app(database_path)) as client:
        with sqlite3.connect(database_path) as connection:
            connection.execute("DROP TABLE tasks")

        assert client.get("/health").status_code == 503


def test_database_path_can_be_configured_by_environment(tmp_path, monkeypatch):
    database_path = tmp_path / "environment" / "configured.db"
    monkeypatch.setenv("TASKFLOW_DB_PATH", str(database_path))

    with TestClient(create_app()) as client:
        assert client.get("/health").status_code == 200

    assert database_path.is_file()


def test_openapi_documents_api_contract(client):
    schema = client.get("/openapi.json").json()
    assert schema["info"]["title"] == "TaskFlow API"
    assert "201" in schema["paths"]["/tasks"]["post"]["responses"]
    assert "404" in schema["paths"]["/tasks/{task_id}"]["patch"]["responses"]
    assert "503" in schema["paths"]["/health"]["get"]["responses"]
