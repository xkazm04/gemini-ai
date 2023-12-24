from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def create_user(self):
        self.client.post("/user", json={"username": "test_user"})