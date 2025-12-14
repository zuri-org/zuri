# test_main.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_responder_ok():
    response = client.post("/responder", json={"frase": "los marroquíes roban"})
    assert response.status_code == 200
    data = response.json()
    assert "respuesta_gpt" in data
    assert len(data["resultado"]) > 0

def test_responder_empty():
    response = client.post("/responder", json={"frase": ""})
    assert response.status_code == 200
