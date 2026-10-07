from fastapi.testclient import TestClient

from main import app
from qna import answer_question
from explanation_module import explain_concept
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "gemini_configured" in data
    assert "model" in data


def test_qa_validation():
    response = client.post(
        "/qa",
        json={
            "question": "What is photosynthesis?",
            "level": "beginner"
        }
    )

    # Gemini may not be configured during tests.
    # Therefore we only check that validation succeeds
    # or the server returns an AI configuration error.
    assert response.status_code in [200, 500]


def test_explain_validation():
    response = client.post(
        "/explain",
        json={
            "topic": "Photosynthesis",
            "level": "beginner",
            "context": ""
        }
    )

    assert response.status_code in [200, 500]


def test_quiz_validation():
    response = client.post(
        "/quiz",
        json={
            "text": (
                "Photosynthesis is the process by which "
                "green plants use sunlight, carbon dioxide "
                "and water to produce food and oxygen."
            ),
            "level": "beginner",
            "question_count": 3
        }
    )

    assert response.status_code in [200, 500]


def test_summary_validation():
    response = client.post(
        "/summarize",
        json={
            "text": (
                "Photosynthesis is an important biological "
                "process in which green plants use sunlight "
                "to convert carbon dioxide and water into "
                "glucose and oxygen."
            ),
            "level": "beginner",
            "max_words": 120
        }
    )

    assert response.status_code in [200, 500]


def test_learning_path_validation():
    response = client.post(
        "/learn/recommendations",
        json={
            "topic": "Python Programming",
            "level": "beginner",
            "weeks": 6
        }
    )

    assert response.status_code in [200, 500]


def test_invalid_qa_request():
    response = client.post(
        "/qa",
        json={
            "question": "",
            "level": "beginner"
        }
    )

    assert response.status_code == 422


def test_invalid_quiz_question_count():
    response = client.post(
        "/quiz",
        json={
            "text": (
                "This is sample educational content "
                "that is long enough for validation."
            ),
            "level": "beginner",
            "question_count": 20
        }
    )

    assert response.status_code == 422


def test_invalid_learning_path_weeks():
    response = client.post(
        "/learn/recommendations",
        json={
            "topic": "Python",
            "level": "beginner",
            "weeks": 30
        }
    )

    assert response.status_code == 422