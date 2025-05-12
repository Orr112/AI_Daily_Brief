import pytest 
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("payload,expected_status", [
    ({"topics": ""}, 422),  # Empty topics
    ({"topics": "a" * 1001}, 422),  # Too long
    ({"tone": "casual"}, 422),  # Missing topics
    ({"topics": 12345}, 422),  # Invalid type
    ({"topics": "economy"}, 200),  # Valid, minimal
])


def test_brief_input_validation(mocker, payload, expected_status):
    # Mock OpenAI response so it doesn't make real call
    mocker.patch(
        "app.api.v1.brief_routes.fetch_brief_from_openai",
        return_value="Mocked valid brief"
    )

    response = client.post("/api/v1/briefs", json=payload)
    assert response.status_code == expected_status

def test_get_briefs_default():
    response = client.get("/api/v1/briefs")
    assert response.status_code == 200
    data = response.json()
    assert "briefs" in data
    assert isinstance(data["briefs"], list)
    assert data["limit"] == 10
    assert data["offset"] == 0

def test_get_briefs_custom_limit_offset():
    response = client.get("/api/v1/briefs?limit=2&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 2
    assert data["offset"] == 1
    assert "briefs" in data

def test_post_brief_with_mocked_openai(mocker):
    # Mock OpenAI call
    mock_response = mocker.patch("app.api.v1.brief_routes.fetch_brief_from_openai", return_value="Mocked brief content")

    payload ={
        "topics": "economy and AI",
        "tone": "casual"  
      }
    
    response  = client.post("/api/v1/briefs", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["content"] == "Mocked brief content"
    assert data["id"] > 0
    assert "created_at" in data

def test_post_brief_openai_failure(mocker):
    mocker.patch(
        "app.api.v1.brief_routes.fetch_brief_from_openai",
        side_effect=HTTPException(status_code=500, detail="AI generation failed.")
    )

    payload = {
        "topics": "fail test",
        "tone": "neutral"
    }

    response = client.post("/api/v1/briefs", json=payload)

    data = response.json()
    assert response.status_code == 500
    assert data["error"] == "AI generation failed."
    assert data["status_code"] == 500
    assert "briefs" in data["path"]


def test_post_brief_db_failure(mocker):
    mocker.patch(
        "app.api.v1.brief_routes.fetch_brief_from_openai",
        return_value="Mocked brief content"
    )

    mocker.patch(
        "app.api.v1.brief_routes.insert_brief",
        side_effect=Exception("DB insert failed")
    )

    payload = {"topics": "AI and economy", "tone": "neutral"}

    response = client.post("/api/v1/briefs", json=payload)

    assert response.status_code == 500
    assert response.json() == {
    "error": "Failed to save brief to database.",
    "status_code": 500,
    "path": "http://testserver/api/v1/briefs/"
}


@pytest.mark.usefixtures("caplog")
def test_insert_brief_database_failure(mocker):
    # Arrange: mock OpenAI to return valid content
    mocker.patch(
        "app.api.v1.brief_routes.fetch_brief_from_openai",
        return_value="Mocked content"
    )

    # Mock insert_brief to rase an exception, simulating DB failure
    mocker.patch(
        "app.api.v1.brief_routes.insert_brief",
        side_effect=Exception("Simuted DB error")
    )

    payload = {
        "topics": "AI meets finance",
        "tone": "neutral"
    }

    response = client.post("/api/v1/briefs", json=payload)

    # Assert
    assert response.status_code == 500
    assert response.json() == {
    "error": "Failed to save brief to database.",
    "status_code": 500,
    "path": "http://testserver/api/v1/briefs/"
}
    
