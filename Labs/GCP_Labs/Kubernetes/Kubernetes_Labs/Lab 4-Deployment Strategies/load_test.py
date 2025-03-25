from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    """
    A class representing the behavior of a user for load testing.

    Methods:
    --------
    get():
        Sends a GET request to the root endpoint ("/") and evaluates the response.
        Marks the request as a failure if the status code is not 200, including
        the status code and response text in the failure message. Otherwise, marks
        the request as a success.
    """
    @task
    def get(self):
        with self.client.get("/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed! Status code: {resp.status_code}, Response: {resp.text}")
            else:
                resp.success()

class WebsiteUser(HttpUser):
    """
    WebsiteUser class simulates a user interacting with a web application for load testing purposes.

    Attributes:
        tasks (list): A list of tasks (user behaviors) that the simulated user will perform.
        wait_time (function): A function that defines the wait time between tasks, in this case, between 1 and 2 seconds.
        host (str): The base URL of the web application being tested.
    """
    tasks = [UserBehavior]
    wait_time = between(1, 2)
    host = "http://34.27.39.118"  # Set this to the correct URL where your FastAPI app is running

if __name__ == "__main__":
    import os
    os.system("locust -f load_test.py")
