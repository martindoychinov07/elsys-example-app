import io
import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add repo root to PYTHONPATH so main.py can be imported
sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import app, STORAGE_DIR  # <-- single import after sys.path modification

client = TestClient(app)

# --- Fixture to clear storage after each test ---
@pytest.fixture(autouse=True)
def clear_storage():
    yield
    for f in STORAGE_DIR.iterdir():
        if f.is_file():
            f.unlink()

# --- 1. Test root endpoint ---
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

# --- 2. Test health endpoint ---
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

# --- 3. Test metrics endpoint (empty storage) ---
def test_metrics_empty():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["files_current"] == 0
    assert data["total_storage_bytes"] == 0

# --- 4. Test file upload ---
def test_file_upload():
    file_content = b"Hello world"
    response = client.post("/files", files={"file": ("test.txt", file_content, "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["size"] == len(file_content)
    file_path = STORAGE_DIR / "test.txt"
    assert file_path.exists()
    assert file_path.read_bytes() == file_content

# --- 5. Test file download ---
def test_file_download():
    file_content = b"Download test"
    client.post("/files", files={"file": ("download.txt", file_content, "text/plain")})
    response = client.get("/files/download.txt")
    assert response.status_code == 200
    assert response.content == file_content
    assert response.headers["content-disposition"] == 'attachment; filename="download.txt"'

# --- 6. Test list files ---
def test_list_files():
    client.post("/files", files={"file": ("file1.txt", b"1", "text/plain")})
    client.post("/files", files={"file": ("file2.txt", b"2", "text/plain")})
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert "file1.txt" in data["files"]
    assert "file2.txt" in data["files"]
