from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_greet_with_name():
    response = client.get("/greet/Степан")

    assert response.status_code == 200
    assert response.json() == {"message": "Привет, Степан!"}


def test_greet_with_different_name():
    response = client.get("/greet/Python")

    assert response.status_code == 200
    assert response.json() == {"message": "Привет, Python!"}


def test_show_form_page():
    response = client.get("/form")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Форма" in response.text


def test_submit_form():
    response = client.post("/form", data={"username": "Тест"})

    assert response.status_code == 200
    assert "Привет, Тест!" in response.text


def test_show_upload_page():
    response = client.get("/upload")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Загрузка" in response.text


def test_upload_file():
    file_content = b"Hello, this is test file content!"
    files = {"file": ("test.txt", file_content, "text/plain")}

    response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert "test.txt" in response.text
    assert "Файл загружен" in response.text


def test_nonexistent_endpoint():
    response = client.get("/nonexistent")

    assert response.status_code == 404
