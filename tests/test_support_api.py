from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_is_available():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "customer-support"


def test_support_health_endpoint_is_available():
    response = client.get("/support/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "customer-support"


def test_support_endpoint_handles_billing_request():
    response = client.post(
        "/support/handle",
        json={
            "message": (
                "I was charged twice for my subscription."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "billing"
    assert data["agent"] == "billing"
    assert data["resolved"] is True
    assert data["escalated"] is False


def test_support_endpoint_handles_technical_request():
    response = client.post(
        "/support/handle",
        json={
            "message": (
                "The application crashes when I try to log in."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "technical"
    assert data["agent"] == "technical"


def test_support_endpoint_handles_general_request():
    response = client.post(
        "/support/handle",
        json={
            "message": (
                "I would like to learn more about your service."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "general"
    assert data["agent"] == "general"


def test_support_endpoint_rejects_empty_message():
    response = client.post(
        "/support/handle",
        json={
            "message": "",
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Customer message is required."
    )


def test_support_endpoint_rejects_missing_message():
    response = client.post(
        "/support/handle",
        json={},
    )

    assert response.status_code == 422