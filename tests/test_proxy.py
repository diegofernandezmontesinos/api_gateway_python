import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

client = TestClient(app)

# --- Caso exitoso ---
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_proxy_posts_success(mock_get):
    # Creamos un mock de la respuesta
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "title": "Test post"}]

    # Asignamos el mock al método get
    mock_get.return_value = mock_response

    response = client.get("/proxy/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id"] == 1

# --- Caso recurso no permitido ---
def test_proxy_invalid_resource():
    response = client.get("/proxy/hackers")
    assert response.status_code == 400
    assert response.json()["detail"] == "Recurso no permitido"

# --- Caso error del backend externo ---
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_proxy_backend_error(mock_get):
    mock_get.side_effect = httpx.HTTPError("Error simulado")
    response = client.get("/proxy/posts")
    assert response.status_code == 502
    assert "Error al contactar con servicio externo" in response.json()["detail"]
