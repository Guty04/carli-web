from locust import HttpUser, between, task  # type: ignore


class WebDetonator(HttpUser):
    wait_time = between(5, 15)  # type: ignore

    @task
    def login(self):
        self.client.post("/auth/login", {"username": "Eze412002.eg@gmail.com", "password": "Eze412002"})
