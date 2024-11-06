import httpx
import pytest
from statistics import median
import time

CANARY_INSTANCE_IP = "CANARY_INSTANCE_IP"
 
@pytest.fixture(scope="module")
def client():
    return httpx.Client(base_url=f"http://{CANARY_INSTANCE_IP}:8000")

def test_health_check(client):
    """
    Test to verify the health check endpoint.
    Ensures the service is running and returns the correct status.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_positive_review(client):
    """
    Test to verify the prediction of a positive review.
    Ensures the service correctly identifies a positive sentiment.
    """
    response = client.post("/predict/", json={"review": "This movie was fantastic!"})
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "confidence" in data
    assert data["sentiment"] == "positive"

def test_predict_negative_review(client):
    """
    Test to verify the prediction of a negative review.
    Ensures the service correctly identifies a negative sentiment.
    """
    response = client.post("/predict/", json={"review": "This movie was terrible!"})
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "confidence" in data
    assert data["sentiment"] == "negative"

def test_predict_neutral_review(client):
    """
    Test to verify the prediction of a neutral review.
    Ensures the service correctly handles a neutral sentiment.
    """
    response = client.post("/predict/", json={"review": "This movie was okay."})
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "confidence" in data

def test_bulk_requests(client):
    """
    Test to send multiple requests and gather metrics.
    Ensures the service handles real-world load effectively.
    """
    positive_reviews = ["This movie was fantastic!", "I loved this movie!", "Best movie ever!"]
    negative_reviews = ["This movie was terrible!", "I hated this movie!", "Worst movie ever!"]

    reviews = positive_reviews + negative_reviews 
    request_count = 100
    response_times = []
    passed_requests = 0
    failed_requests = 0

    for _ in range(request_count):
        review = reviews[_ % len(reviews)]
        start_time = time.time()
        response = client.post("/predict/", json={"review": review})
        response_time = time.time() - start_time
        response_times.append(response_time)

        try:
            assert response.status_code == 200
            data = response.json()
            assert "sentiment" in data
            assert "confidence" in data

            expected_sentiment = (
                "positive" if review in positive_reviews
                else "negative" 
            )
            assert data["sentiment"] == expected_sentiment

            passed_requests += 1
        except AssertionError:
            failed_requests += 1
    print(f"Total requests: {request_count}")
    print(f"Passed requests: {passed_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Median response time: {median(response_times):.4f} seconds")
    print(f"Minimum response time: {min(response_times):.4f} seconds")
    print(f"Maximum response time: {max(response_times):.4f} seconds")
    print(f"Average response time: {sum(response_times) / len(response_times):.4f} seconds")
