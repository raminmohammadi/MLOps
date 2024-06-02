from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def predict(self):
        self.client.post("/predict/", json={"review": "This movie was fantastic!"})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)
