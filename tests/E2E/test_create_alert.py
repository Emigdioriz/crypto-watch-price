import pytest
from tests.fixtures.db_fixtures import client

def test_create_alert_success(client):
	payload = {
		"symbol": "BTCUSD",
		"targetPrice": 50000.00
	}
	response = client.post("/alerts/", json=payload)
	assert response.status_code == 201
	data = response.json()
	assert "detail" in data
	assert "id" in data["detail"]
	assert data["detail"]["id"] is not None


def test_create_alert_invalid_price(client):
	payload = {
		"symbol": "BTCUSD",
		"targetPrice": -100.00
	}
	response = client.post("/alerts/", json=payload)
	assert response.status_code == 400
	# Pode validar mensagem de erro se necessário

def test_create_alert_missing_symbol(client):
	payload = {
		"targetPrice": 50000.00
	}
	response = client.post("/alerts/", json=payload)
	assert response.status_code == 422
	assert "detail" in response.json()

def test_create_alert_missing_price(client):
	payload = {
		"symbol": "BTCUSD"
	}
	response = client.post("/alerts/", json=payload)
	assert response.status_code == 422
	assert "detail" in response.json()

def test_create_alert_invalid_symbol_type(client):
	payload = {
		"symbol": 12345,
		"targetPrice": 50000.00
	}
	response = client.post("/alerts/", json=payload)
	assert response.status_code == 422
	assert "detail" in response.json()