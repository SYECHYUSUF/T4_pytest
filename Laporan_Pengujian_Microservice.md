---

# LAPORAN PRAKTIKUM
## PENGUJIAN DAN DEPLOYMENT ARSITEKTUR MICROSERVICES
### Mata Kuliah: Pemrograman Web Lanjutan

---

**Disusun Oleh:**
- Nama  : [Nama Lengkap Anda]
- NIM   : [NIM Anda]
- Kelas : [Kelas Anda]

**Dosen Pengampu:**
[Nama Dosen]

**Program Studi Sistem Informasi**
**Fakultas [Nama Fakultas]**
**[Nama Universitas]**
**2026**

---

## KATA PENGANTAR

Puji syukur penulis panjatkan ke hadirat Tuhan Yang Maha Esa atas berkat dan rahmat-Nya sehingga laporan praktikum ini dapat diselesaikan dengan baik. Laporan ini disusun untuk memenuhi tugas pada mata kuliah Pemrograman Web Lanjutan dengan topik **Pengujian dan Deployment Arsitektur Microservices menggunakan Python**.

Dalam laporan ini, penulis memaparkan proses perancangan, implementasi, dan pengujian sebuah layanan *backend* berbasis FastAPI yang dilengkapi dengan sistem autentikasi JWT, kontrol akses berbasis peran (RBAC), serta operasi CRUD pada entitas Task. Selain itu, laporan ini juga menyajikan hasil pengujian otomatis menggunakan *framework* Pytest dan HTTPX.

Penulis menyadari bahwa laporan ini masih jauh dari sempurna. Oleh karena itu, kritik dan saran yang membangun sangat penulis harapkan demi penyempurnaan di masa mendatang.

[Kota], 25 Maret 2026

Penulis

---

## DAFTAR ISI

1. Pendahuluan
   - 1.1 Latar Belakang
   - 1.2 Tujuan
   - 1.3 Manfaat
2. Landasan Teori
   - 2.1 Arsitektur Microservices
   - 2.2 FastAPI
   - 2.3 JSON Web Token (JWT)
   - 2.4 Role-Based Access Control (RBAC)
   - 2.5 Pytest dan HTTPX
3. Perancangan Sistem
   - 3.1 Struktur Proyek
   - 3.2 Desain Endpoint API
   - 3.3 Alur Autentikasi
4. Implementasi
   - 4.1 Konfigurasi Proyek dan Dependensi
   - 4.2 Implementasi Aplikasi FastAPI (`main.py`)
   - 4.3 Implementasi Test Suite (`test_main.py`)
5. Hasil Pengujian
   - 5.1 Skenario 1: Pengujian Alur Autentikasi
   - 5.2 Skenario 2: Pengujian CRUD Operasional
   - 5.3 Skenario 3: Pengujian RBAC (Access Denied)
   - 5.4 Ringkasan Hasil
6. Pembahasan
7. Kesimpulan dan Saran
8. Daftar Pustaka
9. Lampiran

---

## BAB I — PENDAHULUAN

### 1.1 Latar Belakang

Perkembangan teknologi perangkat lunak dewasa ini mendorong para pengembang untuk beralih dari arsitektur monolitik menuju arsitektur yang lebih modular dan skalabel, salah satunya adalah arsitektur *microservices*. Dalam arsitektur ini, sebuah sistem besar dipecah menjadi sejumlah layanan kecil yang berdiri sendiri, masing-masing bertanggung jawab atas satu fungsi bisnis tertentu dan berkomunikasi satu sama lain melalui antarmuka yang terdefinisi dengan baik, umumnya berbasis HTTP REST API.

Seiring dengan meningkatnya kompleksitas sistem berbasis microservices, kebutuhan terhadap pengujian otomatis yang terstruktur pun semakin meningkat. Pengujian yang komprehensif tidak hanya menjamin kebenaran logika bisnis, tetapi juga memastikan keamanan sistem, terutama pada aspek autentikasi dan otorisasi. Oleh karena itu, praktikum ini dirancang untuk melatih kemampuan mahasiswa dalam membangun sekaligus menguji sebuah layanan *backend* microservice menggunakan Python.

### 1.2 Tujuan

Tujuan dari pelaksanaan praktikum ini adalah sebagai berikut:

1. Membangun sebuah microservice berbasis FastAPI yang dilengkapi dengan sistem autentikasi JWT dan kontrol akses berbasis peran (RBAC).
2. Mengimplementasikan operasi CRUD pada entitas "Task" menggunakan penyimpanan *in-memory*.
3. Merancang dan menjalankan *test suite* otomatis menggunakan Pytest yang mencakup tiga skenario utama, yaitu pengujian alur autentikasi, pengujian operasi CRUD, dan pengujian mekanisme RBAC.
4. Memahami pentingnya pengujian otomatis dalam siklus pengembangan perangkat lunak berbasis microservices.

### 1.3 Manfaat

Manfaat yang diperoleh dari praktikum ini antara lain:

- Mahasiswa mampu mengembangkan REST API yang aman menggunakan FastAPI dan JWT.
- Mahasiswa memahami konsep RBAC dan cara penerapannya dalam sebuah API.
- Mahasiswa terampil dalam menulis *test case* otomatis menggunakan Pytest, sehingga dapat menerapkan praktik *Test-Driven Development* (TDD) dalam proyek nyata.

---

## BAB II — LANDASAN TEORI

### 2.1 Arsitektur Microservices

Arsitektur *microservices* adalah sebuah pendekatan pengembangan perangkat lunak yang menyusun aplikasi sebagai kumpulan layanan kecil yang saling independen. Setiap layanan menjalankan prosesnya sendiri, berkomunikasi melalui mekanisme yang ringan (biasanya HTTP REST atau *message broker*), dan dapat di-*deploy* secara independen. Kelebihan utama arsitektur ini meliputi skalabilitas tinggi, kemudahan pemeliharaan, dan toleransi kesalahan yang lebih baik dibandingkan arsitektur monolitik.

### 2.2 FastAPI

FastAPI adalah *web framework* modern berbasis Python yang dirancang untuk membangun API dengan performa tinggi. FastAPI memanfaatkan fitur *type hints* dari Python 3.6+ dan library Pydantic untuk validasi data secara otomatis. Salah satu keunggulan FastAPI adalah kemampuannya menghasilkan dokumentasi interaktif (Swagger UI dan ReDoc) secara otomatis berdasarkan kode yang ditulis. FastAPI juga mendukung penuh operasi asinkron (*async/await*), menjadikannya pilihan yang sangat tepat untuk membangun microservice yang responsif.

### 2.3 JSON Web Token (JWT)

JSON Web Token (JWT) adalah standar terbuka (RFC 7519) yang mendefinisikan cara yang ringkas dan mandiri untuk mengirimkan informasi antar pihak dalam bentuk objek JSON yang telah ditandatangani secara digital. JWT terdiri dari tiga bagian yang dipisahkan oleh titik: **Header**, **Payload**, dan **Signature**. Dalam konteks autentikasi API, JWT umumnya digunakan sebagai *access token* yang dikirimkan pada setiap permintaan HTTP melalui header `Authorization: Bearer <token>`. Server kemudian memverifikasi token tersebut untuk mengidentifikasi pengguna yang sedang beraktivitas.

### 2.4 Role-Based Access Control (RBAC)

*Role-Based Access Control* (RBAC) adalah sebuah mekanisme kontrol akses yang memberikan izin kepada pengguna berdasarkan peran (*role*) yang dimilikinya, bukan berdasarkan identitas individu secara langsung. Pada praktikum ini, terdapat dua peran yang diimplementasikan:

- **admin**: Memiliki akses penuh terhadap seluruh endpoint, termasuk operasi *create*, *update*, dan *delete*.
- **user**: Hanya memiliki akses *read-only* terhadap data; tidak diizinkan melakukan perubahan data. Setiap percobaan mengakses endpoint yang dibatasi akan mendapatkan respons `403 Forbidden`.

### 2.5 Pytest dan HTTPX / TestClient

Pytest adalah *testing framework* untuk Python yang terkenal karena kemudahannya dalam penulisan *test case* serta laporan hasil yang informatif. Pada praktikum ini, digunakan `TestClient` dari FastAPI (yang secara internal menggunakan `httpx`) untuk mensimulasikan permintaan HTTP ke aplikasi tanpa perlu menjalankan server sungguhan. Hal ini memungkinkan pengujian dilakukan secara cepat, terisolasi, dan dapat diulang dengan hasil yang konsisten (*deterministic*).

---

## BAB III — PERANCANGAN SISTEM

### 3.1 Struktur Proyek

Struktur direktori proyek ini dirancang secara sederhana namun terorganisir agar mudah dipahami dan dikembangkan lebih lanjut. Berikut adalah susunannya:

```
T4_WEB/
├── main.py               # Aplikasi FastAPI (Auth + CRUD + RBAC)
├── requirements.txt      # Daftar dependensi Python
├── pytest.ini            # Konfigurasi Pytest
├── Readme.md             # Panduan penggunaan proyek
└── tests/
    ├── __init__.py       # Penanda paket Python
    └── test_main.py      # Test suite (19 test case)
```

> **[LAMPIRAN SCREENSHOT 1]**
> *Tempelkan di sini: Screenshot tampilan struktur folder proyek di VS Code atau terminal (`ls -la` atau `tree`).*

### 3.2 Desain Endpoint API

Tabel berikut merangkum seluruh endpoint yang tersedia dalam microservice ini beserta hak akses yang berlaku untuk setiap peran.

| No | Method | Endpoint          | Role yang Diizinkan | Deskripsi                               |
|----|--------|-------------------|-----------------------|-----------------------------------------|
| 1  | POST   | `/register`       | Public                | Registrasi pengguna baru                |
| 2  | POST   | `/login`          | Public                | Login dan mendapatkan JWT *access token*|
| 3  | GET    | `/tasks`          | `admin`, `user`       | Mengambil semua data Task               |
| 4  | GET    | `/tasks/{id}`     | `admin`, `user`       | Mengambil data Task berdasarkan ID      |
| 5  | POST   | `/tasks`          | `admin` saja          | Membuat Task baru                       |
| 6  | PUT    | `/tasks/{id}`     | `admin` saja          | Memperbarui data Task                   |
| 7  | DELETE | `/tasks/{id}`     | `admin` saja          | Menghapus Task                          |

### 3.3 Alur Autentikasi

Alur autentikasi dalam sistem ini berjalan sebagai berikut:

1. Pengguna melakukan registrasi melalui endpoint `POST /register` dengan memberikan `username`, `password`, dan `role`.
2. Server menyimpan data pengguna dengan kata sandi yang telah di-*hash* menggunakan algoritma `sha256_crypt`.
3. Pengguna melakukan login melalui endpoint `POST /login`. Jika kredensial valid, server membuat dan mengembalikan *access token* berformat JWT yang berisi klaim `sub` (username) dan `role`.
4. Untuk setiap permintaan ke endpoint yang terproteksi, pengguna menyertakan token pada header HTTP: `Authorization: Bearer <token>`.
5. Server mendekode token, memverifikasi validitasnya, dan memeriksa peran pengguna sebelum mengizinkan akses ke sumber daya yang diminta.

---

## BAB IV — IMPLEMENTASI

### 4.1 Konfigurasi Proyek dan Dependensi

Proyek ini menggunakan sejumlah *library* Python yang dikelola melalui virtual environment. Perintah berikut digunakan untuk mempersiapkan lingkungan pengembangan:

```bash
# Membuat virtual environment
python3 -m venv venv

# Mengaktifkan virtual environment (macOS/Linux)
source venv/bin/activate

# Menginstal seluruh dependensi
pip install -r requirements.txt
```

Isi file `requirements.txt` yang mendefinisikan dependensi proyek adalah sebagai berikut:

```
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
anyio>=4.0.0
```

> **[LAMPIRAN SCREENSHOT 2]**
> *Tempelkan di sini: Screenshot terminal setelah menjalankan `pip install -r requirements.txt` yang menunjukkan proses instalasi berhasil.*

### 4.2 Implementasi Aplikasi FastAPI (`main.py`)

File `main.py` merupakan inti dari microservice ini. Implementasinya mencakup beberapa komponen utama yang dijelaskan di bawah ini.

#### 4.2.1 Inisialisasi Aplikasi dan Konfigurasi JWT

Aplikasi FastAPI diinisialisasi bersama dengan konfigurasi konstanta JWT, yaitu `SECRET_KEY` sebagai kunci rahasia penandatanganan token, `ALGORITHM` yang menggunakan standar HS256, serta `ACCESS_TOKEN_EXPIRE_MINUTES` yang menentukan durasi validitas token.

```python
SECRET_KEY = "supersecretkey_ganti_di_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Microservice API", version="1.0.0")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
```

#### 4.2.2 Mock Database (In-Memory)

Sebagai pengganti database yang sesungguhnya, digunakan dua buah *dictionary* Python untuk menyimpan data pengguna dan task secara sementara selama aplikasi berjalan:

```python
fake_users_db: dict = {}   # Menyimpan data user
fake_tasks_db: dict = {}   # Menyimpan data task
task_id_counter: int = 1   # Counter ID task (auto-increment)
```

#### 4.2.3 Dependency RBAC

Mekanisme RBAC diimplementasikan sebagai fungsi *dependency* FastAPI. Fungsi `require_admin` memanggil `get_current_user` terlebih dahulu untuk mengidentifikasi pengguna, kemudian memeriksa apakah perannya adalah `admin`. Jika bukan, server secara otomatis mengembalikan respons `403 Forbidden`.

```python
def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied",
        )
    return current_user
```

> **[LAMPIRAN SCREENSHOT 3]**
> *Tempelkan di sini: Screenshot tampilan file `main.py` yang terbuka di editor kode (VS Code), menampilkan keseluruhan atau bagian penting dari kode.*

#### 4.2.4 Tampilan Dokumentasi Swagger UI

FastAPI secara otomatis menghasilkan dokumentasi interaktif yang dapat diakses melalui browser setelah server dijalankan dengan perintah `uvicorn main:app --reload`.

> **[LAMPIRAN SCREENSHOT 4]**
> *Tempelkan di sini: Screenshot tampilan Swagger UI (`http://127.0.0.1:8000/docs`) yang menampilkan seluruh endpoint yang telah dibuat.*

### 4.3 Implementasi Test Suite (`test_main.py`)

File `test_main.py` berisi 19 *test case* yang diorganisasi ke dalam tiga kelas sesuai skenario pengujian. Beberapa strategi penting yang diterapkan dalam penulisan *test suite* ini adalah:

**Test Isolation**: Setiap test dijalankan dengan state database yang bersih berkat penggunaan *fixture* `reset_db` dengan parameter `autouse=True`. Fixture ini aktif secara otomatis sebelum dan sesudah setiap test case.

```python
@pytest.fixture(autouse=True)
def reset_db():
    fake_users_db.clear()
    fake_tasks_db.clear()
    app_module.task_id_counter = 1
    yield
    fake_users_db.clear()
    fake_tasks_db.clear()
    app_module.task_id_counter = 1
```

**Reusable Fixtures**: Token autentikasi untuk admin dan user biasa dipersiapkan sebagai *fixture* yang dapat dipakai ulang di seluruh test case, sehingga tidak terjadi duplikasi kode.

```python
@pytest.fixture
def admin_token(client):
    client.post("/register", json={"username": "admin1", "password": "adminpass", "role": "admin"})
    res = client.post("/login", data={"username": "admin1", "password": "adminpass"})
    return res.json()["access_token"]
```

> **[LAMPIRAN SCREENSHOT 5]**
> *Tempelkan di sini: Screenshot tampilan file `test_main.py` yang terbuka di editor kode, menampilkan struktur kelas dan beberapa test case.*

---

## BAB V — HASIL PENGUJIAN

Pengujian dilakukan dengan menjalankan Pytest dari direktori *root* proyek menggunakan perintah berikut:

```bash
pytest tests/test_main.py -v
```

Berikut adalah penjelasan masing-masing skenario beserta hasil yang diperoleh.

### 5.1 Skenario 1: Pengujian Alur Autentikasi

Skenario pertama bertujuan untuk memverifikasi bahwa seluruh alur autentikasi, mulai dari registrasi hingga perolehan token, berjalan sesuai dengan yang diharapkan. Terdapat 6 (enam) *test case* dalam skenario ini.

| No | Nama Test Case                          | Kondisi Uji                                      | Ekspektasi           | Hasil  |
|----|-----------------------------------------|--------------------------------------------------|----------------------|--------|
| 1  | `test_register_success`                 | Registrasi user baru dengan data valid           | Status 201, data user dikembalikan | ✅ PASSED |
| 2  | `test_register_duplicate_username`      | Registrasi dengan username yang sudah terdaftar  | Status 400 Bad Request             | ✅ PASSED |
| 3  | `test_register_invalid_role`            | Registrasi dengan role tidak valid ("superuser") | Status 422 Unprocessable Entity    | ✅ PASSED |
| 4  | `test_login_returns_valid_token`        | Login dengan kredensial yang benar               | Status 200, token JWT dikembalikan | ✅ PASSED |
| 5  | `test_login_wrong_password`             | Login dengan kata sandi yang salah               | Status 401 Unauthorized            | ✅ PASSED |
| 6  | `test_login_unknown_user`               | Login dengan username yang tidak terdaftar       | Status 401 Unauthorized            | ✅ PASSED |

> **[LAMPIRAN SCREENSHOT 6]**
> *Tempelkan di sini: Screenshot output terminal yang menampilkan hasil test skenario 1 (TestAuthFlow) dengan status PASSED.*

### 5.2 Skenario 2: Pengujian CRUD Operasional

Skenario kedua bertujuan untuk memverifikasi bahwa seluruh operasi CRUD pada entitas Task dapat dilakukan dengan benar oleh pengguna berperan `admin`. Terdapat 8 (delapan) *test case* dalam skenario ini.

| No | Nama Test Case                   | Kondisi Uji                                              | Ekspektasi                        | Hasil     |
|----|----------------------------------|----------------------------------------------------------|-----------------------------------|-----------|
| 1  | `test_create_task`               | POST /tasks dengan data valid sebagai admin              | Status 201, task baru dikembalikan | ✅ PASSED |
| 2  | `test_read_all_tasks`            | GET /tasks setelah membuat 2 task                        | Status 200, list berisi 2 task    | ✅ PASSED |
| 3  | `test_read_single_task`          | GET /tasks/{id} dengan ID yang valid                     | Status 200, task yang tepat dikembalikan | ✅ PASSED |
| 4  | `test_read_task_not_found`       | GET /tasks/9999 (ID tidak ada)                           | Status 404 Not Found              | ✅ PASSED |
| 5  | `test_update_task`               | PUT /tasks/{id} dengan data baru yang lengkap            | Status 200, data task terupdate   | ✅ PASSED |
| 6  | `test_update_task_partial`       | PUT /tasks/{id} hanya memperbarui field `title`          | Status 200, `description` tidak berubah | ✅ PASSED |
| 7  | `test_delete_task`               | DELETE /tasks/{id} dengan ID yang valid                  | Status 200, task terhapus; GET berikutnya 404 | ✅ PASSED |
| 8  | `test_delete_task_not_found`     | DELETE /tasks/9999 (ID tidak ada)                        | Status 404 Not Found              | ✅ PASSED |

> **[LAMPIRAN SCREENSHOT 7]**
> *Tempelkan di sini: Screenshot output terminal yang menampilkan hasil test skenario 2 (TestCRUDAdmin) dengan status PASSED.*

### 5.3 Skenario 3: Pengujian RBAC (Access Denied)

Skenario ketiga merupakan inti dari pengujian keamanan. Skenario ini memverifikasi bahwa pengguna dengan peran `user` tidak dapat mengakses endpoint yang dibatasi, serta memastikan bahwa pengguna yang tidak terautentikasi sama sekali tidak dapat mengakses endpoint manapun. Terdapat 5 (lima) *test case* dalam skenario ini.

| No | Nama Test Case                                | Kondisi Uji                                         | Ekspektasi                     | Hasil     |
|----|-----------------------------------------------|-----------------------------------------------------|--------------------------------|-----------|
| 1  | `test_user_cannot_create_task`                | POST /tasks sebagai user biasa                      | Status 403 Forbidden, detail "Access Denied" | ✅ PASSED |
| 2  | `test_user_cannot_update_task`                | PUT /tasks/{id} sebagai user biasa                  | Status 403 Forbidden, detail "Access Denied" | ✅ PASSED |
| 3  | `test_user_cannot_delete_task`                | DELETE /tasks/{id} sebagai user biasa               | Status 403 Forbidden, detail "Access Denied" | ✅ PASSED |
| 4  | `test_user_can_read_tasks`                    | GET /tasks sebagai user biasa                       | Status 200 (diizinkan)         | ✅ PASSED |
| 5  | `test_unauthenticated_cannot_access_tasks`    | GET /tasks tanpa token sama sekali                  | Status 401 Unauthorized        | ✅ PASSED |

> **[LAMPIRAN SCREENSHOT 8]**
> *Tempelkan di sini: Screenshot output terminal yang menampilkan hasil test skenario 3 (TestRBACAccessDenied) dengan status PASSED.*

### 5.4 Ringkasan Hasil Keseluruhan

Seluruh pengujian telah berhasil dijalankan dengan hasil yang memuaskan. Ringkasan akhir adalah sebagai berikut:

| Skenario                    | Jumlah Test | Lulus (Passed) | Gagal (Failed) |
|----------------------------|-------------|----------------|----------------|
| Alur Autentikasi           | 6           | 6              | 0              |
| CRUD Operasional (Admin)   | 8           | 8              | 0              |
| RBAC (Access Denied)       | 5           | 5              | 0              |
| **Total**                  | **19**      | **19**         | **0**          |

> **[LAMPIRAN SCREENSHOT 9]**
> *Tempelkan di sini: Screenshot output terminal lengkap yang menampilkan hasil akhir seluruh 19 test case dengan laporan "19 passed" dari Pytest.*

---

## BAB VI — PEMBAHASAN

### 6.1 Ketepatan Implementasi JWT

Implementasi JWT pada proyek ini mengikuti alur standar yang umum digunakan pada aplikasi produksi. Token yang dihasilkan memuat klaim `sub` (username) dan `role` pada bagian *payload*, sehingga server dapat mengidentifikasi identitas dan hak akses pengguna hanya dari informasi yang terkandung dalam token tanpa perlu melakukan kueri ke database pada setiap permintaan. Pendekatan *stateless* ini merupakan salah satu keunggulan utama JWT dibandingkan mekanisme autentikasi berbasis sesi (*session-based*).

### 6.2 Efektivitas Mekanisme RBAC

Mekanisme RBAC yang diimplementasikan melalui sistem *dependency injection* FastAPI terbukti bekerja secara efektif. Penggunaan fungsi `require_admin` sebagai *dependency* pada endpoint yang dilindungi memungkinkan penerapan kontrol akses yang bersih dan tidak mengotori logika bisnis utama. Hasil dari Skenario 3 mengonfirmasi bahwa sistem berhasil menolak seluruh upaya akses tidak sah dari pengguna berperan `user`, sekaligus memberikan izin akses *read* yang seharusnya dimiliki oleh role tersebut.

### 6.3 Kualitas Test Suite

Test suite yang dikembangkan memiliki beberapa karakteristik yang mencerminkan praktik pengujian yang baik:

- **Isolasi** (*Test Isolation*): Setiap *test case* berjalan pada state yang bersih, menghilangkan risiko kegagalan yang disebabkan oleh efek samping antar-test.
- **Komprehensif**: Pengujian tidak hanya mencakup *happy path* (kondisi sukses), tetapi juga *edge case* seperti input tidak valid, ID yang tidak ditemukan, dan akses yang tidak terotorisasi.
- **Keterbacaan**: Penamaan *test case* yang deskriptif dan pengorganisasian ke dalam kelas memudahkan pembaca untuk memahami tujuan dari setiap pengujian tanpa perlu membaca detail implementasinya.

### 6.4 Catatan Teknis: Kompatibilitas Bcrypt pada Python 3.14

Selama proses pengembangan, ditemukan ketidaksesuaian (*incompatibility*) antara library `passlib` versi terbaru dan library `bcrypt` pada lingkungan Python 3.14. Masalah ini muncul karena `passlib` mencoba menjalankan prosedur deteksi bug pada `bcrypt` secara internal menggunakan kata sandi sintetis yang melebihi batas 72 byte, yang justru memicu pengecualian (*exception*) pada `bcrypt` versi baru.

Sebagai solusi, skema hashing diganti menjadi `sha256_crypt` yang sepenuhnya didukung oleh `passlib` pada semua versi Python terkini, tanpa mengurangi tingkat keamanan yang relevan untuk keperluan praktikum ini.

---

## BAB VII — KESIMPULAN DAN SARAN

### 7.1 Kesimpulan

Berdasarkan hasil implementasi dan pengujian yang telah dilakukan, dapat ditarik beberapa kesimpulan sebagai berikut:

1. Pengembangan microservice backend menggunakan FastAPI dapat dilakukan secara cepat dan efisien berkat dukungan validasi data otomatis, sistem *dependency injection*, dan pembuatan dokumentasi API yang terintegrasi.
2. Sistem autentikasi berbasis JWT berhasil diimplementasikan dan terbukti berfungsi dengan baik, di mana server mampu mengidentifikasi identitas dan peran pengguna secara *stateless* hanya dari informasi yang terkandung dalam token.
3. Mekanisme RBAC berhasil membatasi akses pengguna berperan `user` terhadap operasi yang bersifat mutasi data (POST, PUT, DELETE), sementara akses *read-only* tetap diberikan sebagaimana mestinya.
4. Seluruh 19 *test case* dalam test suite berhasil dijalankan dengan hasil lulus (PASSED), membuktikan bahwa seluruh komponen sistem berfungsi sesuai dengan spesifikasi yang telah ditetapkan.

### 7.2 Saran

Untuk pengembangan lebih lanjut, penulis menyarankan beberapa perbaikan berikut:

1. **Database Permanen**: Mengintegrasikan sistem dengan database relasional (misalnya PostgreSQL menggunakan SQLAlchemy atau Tortoise ORM) untuk menggantikan penyimpanan *in-memory* yang bersifat sementara.
2. **Pengujian Coverage**: Menambahkan laporan *code coverage* menggunakan `pytest-cov` untuk mengukur seberapa banyak baris kode yang telah tercakup oleh pengujian.
3. **Token Refresh**: Mengimplementasikan mekanisme *refresh token* agar pengguna tidak perlu login ulang setiap kali *access token* kedaluwarsa.
4. **Containerisasi**: Mem-*package* aplikasi ke dalam kontainer Docker untuk mempermudah proses *deployment* ke berbagai lingkungan produksi.

---

## DAFTAR PUSTAKA

1. FastAPI. (2024). *FastAPI Documentation*. Tiangolo. Diakses dari https://fastapi.tiangolo.com/
2. Pytest. (2024). *pytest: helps you write better programs*. Diakses dari https://docs.pytest.org/
3. Jones, M., Bradley, J., & Sakimura, N. (2015). *JSON Web Token (JWT)* (RFC 7519). Internet Engineering Task Force (IETF). Diakses dari https://www.rfc-editor.org/rfc/rfc7519
4. OWASP. (2023). *REST Security Cheat Sheet*. OWASP Foundation. Diakses dari https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
5. Richardson, C., & Smith, F. (2019). *Microservices Patterns*. Manning Publications.

---

## LAMPIRAN

> **Catatan untuk Penyusun Laporan:**
> Tempatkan setiap screenshot di bawah keterangan lampiran yang sesuai, sesuai urutan yang telah ditandai pada bab-bab sebelumnya. Setiap gambar sebaiknya diberi nomor, judul, dan keterangan singkat.

---

**Lampiran 1 — Struktur Folder Proyek**
*(Tempelkan screenshot struktur folder T4_WEB di VS Code atau hasil perintah `tree` di terminal)*

---

**Lampiran 2 — Proses Instalasi Dependensi**
*(Tempelkan screenshot terminal setelah perintah `pip install -r requirements.txt`)*

---

**Lampiran 3 — Kode Sumber `main.py`**
*(Tempelkan screenshot tampilan file `main.py` di editor kode)*

---

**Lampiran 4 — Tampilan Swagger UI**
*(Tempelkan screenshot halaman `http://127.0.0.1:8000/docs` di browser)*

---

**Lampiran 5 — Kode Sumber `test_main.py`**
*(Tempelkan screenshot tampilan file `test_main.py` di editor kode)*

---

**Lampiran 6 — Hasil Test Skenario 1: Autentikasi**
*(Tempelkan screenshot output terminal yang menunjukkan 6 test PASSED untuk kelas TestAuthFlow)*

---

**Lampiran 7 — Hasil Test Skenario 2: CRUD Admin**
*(Tempelkan screenshot output terminal yang menunjukkan 8 test PASSED untuk kelas TestCRUDAdmin)*

---

**Lampiran 8 — Hasil Test Skenario 3: RBAC**
*(Tempelkan screenshot output terminal yang menunjukkan 5 test PASSED untuk kelas TestRBACAccessDenied)*

---

**Lampiran 9 — Hasil Akhir Seluruh Test Suite**
*(Tempelkan screenshot output terminal lengkap yang menampilkan "19 passed" di baris terakhir)*

---

*— Akhir Dokumen Laporan —*
