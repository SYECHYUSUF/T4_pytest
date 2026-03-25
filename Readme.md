# Task Management API

Aplikasi backend berbasis REST API untuk manajemen tugas (*Task Management*) yang dibangun menggunakan FastAPI. Proyek ini dilengkapi dengan fitur autentikasi JWT dan Role-Based Access Control (RBAC).

## Fitur Utama

- **Autentikasi & Otorisasi**: Login dan proteksi endpoint menggunakan token JWT.
- **RBAC (Role-Based Access Control)**: 
  - `admin`: Memiliki akses penuh untuk melakukan operasi CRUD (Create, Read, Update, Delete) pada task.
  - `user`: Hanya memiliki akses baca (Read) data task.
- **CRUD Operations**: Mengelola kelengkapan data task di dalam sistem (menggunakan penyimpanan in-memory).

## Persyaratan Sistem

- Python 3.8 atau lebih baru
- Pip (Python package installer)

## Cara Menjalankan Aplikasi di Lokal

1. **Siapkan folder proyek**
   Buka terminal/command prompt dan masuk ke dalam folder proyek ini.

2. **Buat Virtual Environment (Sangat disarankan)**
   ```bash
   python -m venv venv
   ```
   Aktifkan virtual environment:
   - Pengguna Windows: `venv\Scripts\activate`
   - Pengguna MacOS/Linux: `source venv/bin/activate`

3. **Install Dependensi**
   Install semua library yang dibutuhkan melalui file `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Server**
   Jalankan aplikasi FastAPI menggunakan *app server* Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   Jika berhasil, terminal akan menampilkan pesan bahwa aplikasi berjalan di `http://127.0.0.1:8000`.

---

## Cara Menggunakan dan Uji Coba API (via Swagger UI)

Kelebihan utama menggunakan FastAPI adalah dokumentasi API interaktif (Swagger UI) yang di-generate secara otomatis. Kamu tidak perlu lagi repot-repot setup Postman untuk sekadar mencoba API.

Berikut langkah-langkah mudah untuk melakukan pengetesan:

1. Buka browser dan kunjungi alamat **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.
2. Di sana akan muncul daftar semua URL endpoint API yang tersedia.

### Panduan Testing:

**Langkah 1: Buat Akun (Register)**
- Cari baris endpoint `POST /register`.
- Klik untuk membuka detailnya, lalu tekan tombol **"Try it out"** di sebelah kanan.
- Ubah/isi data pada kolom *Request body*. Contohnya:
  ```json
  {
    "username": "admin1",
    "password": "password123",
    "role": "admin"
  }
  ```
  *(Note: Untuk kolom role bisa kamu isi "admin" atau "user")*
- Klik tombol **"Execute"**. Scroll sikit ke bawah untuk melihat respons server (pastikan dapat kode `201`).

**Langkah 2: Login agar bisa akses endpoint lainnya**
- Scroll ke paling atas halaman dokumentasi. Kamu akan melihat tombol **"Authorize"** dengan ikon gembok berwarna hijau. Klik tombol tersebut.
- Akan muncul pop-up login. Masukkan `username` dan `password` akun yang baru saja kamu buat tadi.
- Klik **"Authorize"** lalu klik "Close". 
- *Congrats!* Sekarang kamu sudah masuk, dan setiap requset ke API selanjutnya akan otomatis menyertakan token JWT.

**Langkah 3: Coba Fitur CRUD Task**
- **Lihat Data Task**: Buka `GET /tasks`, klik "Try it out", kosongkan saja isiannya lalu klik "Execute". (Bisa diakses role apa saja).
- **Buat Task Baru**: Buka `POST /tasks`, klik "Try it out", ketik JSON soal task baru (title, description), lalu "Execute". (Hanya berhasil untuk login role `admin`).
- **Update Task**: Buka `PUT /tasks/{id}`, masukkan ID dari task yang mau di-update beserta form data barunya.
- **Hapus Data**: Buka `DELETE /tasks/{id}`, isikan ID yang dibidik untuk dihapus. 

*Silakan bereksperimen: Coba daftar akun lagi dengan role "user", lalu coba pakai akun tersebut untuk menghapus task atau menambah task baru. Server pasti akan menolak dengan memunculkan pesan error `403 Forbidden` (Akses ditolak).*

---

## Cara Menjalankan Automated Testing

Daripada cek satu-satu manual, proyek ini sudah dilengkapi *test suite* berisi belasan skenario pengujian otomatis menggunakan Pytest.

Untuk menjalankan testing secara keseluruhan:
```bash
pytest tests/test_main.py -v
```
Atau jika ingin lebih ringkas bisa dengan:
```bash
pytest
```

Nanti di terminal akan keluar laporan detail tentang status passing dari skenario *auth*, *crud validation*, sampai ke batasan hak akses *RBAC*.
