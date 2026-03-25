import pytest
from fastapi.testclient import TestClient

# ==========================================
# CATATAN PENTING UNTUK MAHASISWA:
# 1. Pastikan Anda mengimpor aplikasi FastAPI Anda di sini.
#    Contoh: from main import app
# 2. Sesuaikan nama endpoint (URL) dengan yang ada di microservice Anda.
# 3. Sesuaikan struktur payload JSON sesuai model Pydantic Anda.
# ==========================================

# Mock import app (Silakan buka komentar di bawah ini dan hapus mock client jika diintegrasikan)
# from main import app
# client = TestClient(app)

# --- MOCK CLIENT SEMENTARA UNTUK TUJUAN DOKUMENTASI ---
# Hapus blok ini di project aslinya
from fastapi import FastAPI
app = FastAPI()
client = TestClient(app)
# ----------------------------------------------------

# Data dummy untuk pengujian
test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "strongpassword123",
    "role": "user" # Role default
}

test_admin = {
    "username": "adminuser",
    "email": "admin@example.com",
    "password": "adminpassword123",
    "role": "admin"
}

# ==========================================
# BAGIAN 1: PENGUJIAN AUTENTIKASI (Register/Login)
# ==========================================

def test_register_user():
    """Menguji endpoint pendaftaran pengguna baru"""
    response = client.post(
        "/auth/register", # Sesuaikan URL endpoint Anda
        json=test_user
    )
    # Asumsi status sukses pembuatan data adalah 201 atau 200
    assert response.status_code in [200, 201], f"Gagal register: {response.text}"
    data = response.json()
    assert "username" in data
    assert data["username"] == test_user["username"]

def test_login_user():
    """Menguji endpoint login dan pengambilan JWT token"""
    # Menggunakan form-data jika login pakai OAuth2PasswordRequestForm
    response = client.post(
        "/auth/login", # Sesuaikan URL endpoint Anda
        data={
            "username": test_user["username"], 
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200, f"Gagal login: {response.text}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Fixture untuk mendapatkan token saat pengujian lain berjalan
@pytest.fixture(scope="module")
def user_token():
    # Login dulu untuk dapat token
    response = client.post("/auth/login", data={"username": test_user["username"], "password": test_user["password"]})
    if response.status_code != 200:
        return "fake_user_token" # fallback jika DB mock
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def admin_token():
    # Login sebagai admin
    response = client.post("/auth/login", data={"username": test_admin["username"], "password": test_admin["password"]})
    if response.status_code != 200:
        return "fake_admin_token" # fallback jika DB mock
    return response.json()["access_token"]


# ==========================================
# BAGIAN 2: PENGUJIAN CRUD OPERASIONAL
# ==========================================

def test_create_item(user_token):
    """Menguji endpoint POST (Create) dengan Auth Token"""
    headers = {"Authorization": f"Bearer {user_token}"}
    item_payload = {
        "name": "Barang Test",
        "description": "Deskripsi barang test",
        "price": 50000
    }
    
    response = client.post("/items/", json=item_payload, headers=headers)
    assert response.status_code in [200, 201]
    
    data = response.json()
    assert data["name"] == item_payload["name"]
    assert "id" in data # Pastikan ID dikembalikan (auto-increment)

def test_read_items():
    """Menguji endpoint GET (Read) list semua data"""
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list) # Pastikan return-nya array/list

def test_read_item_by_id():
    """Menguji endpoint GET (Read) by ID"""
    # Mengambil item dengan ID 1 (pastikan data ID 1 ada atau sesuaikan ID-nya)
    response = client.get("/items/1")
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert data["id"] == 1
    else:
        assert response.status_code == 404 # Data belum ada di DB mock

def test_update_item(user_token):
    """Menguji endpoint PUT (Update)"""
    headers = {"Authorization": f"Bearer {user_token}"}
    update_payload = {
        "name": "Barang Update",
        "description": "Deskripsi diperbarui",
        "price": 60000
    }
    response = client.put("/items/1", json=update_payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["name"] == "Barang Update"
    else:
        assert response.status_code == 404

def test_delete_item(user_token):
    """Menguji endpoint DELETE"""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.delete("/items/1", headers=headers)
    # Tergantung restriksinya, jika user biasa bisa hapus:
    assert response.status_code in [200, 204, 403, 404]


# ==========================================
# BAGIAN 3: PENGUJIAN RBAC (Access Denied)
# ==========================================

def test_admin_route_access_denied(user_token):
    """Menguji RBAC: User biasa mencoba mengakses endpoint khusus Admin (Harus gagal / 403 Forbidden)"""
    headers = {"Authorization": f"Bearer {user_token}"}
    # Contoh endpoint yang hanya boleh diakses Admin
    response = client.delete("/admin/users/1", headers=headers)
    
    # Harus di-block oleh RBAC
    assert response.status_code == 403, "RBAC Gagal! User biasa bisa mengakses endpoint Admin."
    assert "detail" in response.json()

def test_admin_route_access_success(admin_token):
    """Menguji RBAC: Admin mencoba mengakses endpoint khusus Admin (Harus sukses)"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete("/admin/users/1", headers=headers)
    
    # Asumsi sukses menghapus atau 404 jika data tidak ada, tapi BUKAN 403.
    assert response.status_code != 403, "Admin tidak diizinkan masuk ke endpoint Admin!"
