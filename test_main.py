from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    
def test_create_file():
    response = client.post("/file", json={"data": "test data"})
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}

def test_question_yaml():
    response = client.get("/yaml", params={"question": "test question"})
    assert response.status_code == 200
    # replace with the expected answer
    assert response.json() == {"answer": "expected answer"}

def test_question_pdf():
    response = client.get("/pdf", params={"q": "test question"})
    assert response.status_code == 200
    # replace with the expected answer
    assert response.json() == {"answer": "expected answer"}