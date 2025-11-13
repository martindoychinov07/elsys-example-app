from locust import HttpUser, task, between
from pathlib import Path

class FileStorageUser(HttpUser):
    wait_time = between(1, 3)  # време между заявките (в секунди)

    @task(2)
    def get_root(self):
        self.client.get("/")

    @task(3)
    def list_files(self):
        self.client.get("/files")

    @task(1)
    def health_check(self):
        self.client.get("/health")

    @task(1)
    def upload_file(self):
        # Качваме малък тестов файл
        file_content = b"Locust load test"
        files = {"file": ("locust.txt", file_content, "text/plain")}
        self.client.post("/files", files=files)
