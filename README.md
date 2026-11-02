# Sistem Manajemen Perpustakaan

Aplikasi desktop modern berbasis Python untuk pengelolaan data perpustakaan dengan antarmuka grafis (GUI) yang dirancang menggunakan pustaka **CustomTkinter** serta menerapkan arsitektur **Model-View-Controller (MVC)**. Aplikasi ini dilengkapi dengan sistem **Autentikasi (SHA-256)** dan **Otorisasi Role (RBAC)** antara peran **Admin (Petugas)** dan **Anggota (Mahasiswa)**.

---

## Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Struktur Direktori (MVC)](#struktur-direktori-mvc)
- [Panduan Instalasi & Konfigurasi Database MySQL](#panduan-instalasi--konfigurasi-database-mysql)
- [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
- [Pengujian Otomatis & Linting](#pengujian-otomatis--linting)
- [Kompilasi Executable (.exe)](#kompilasi-executable-exe)

---

## Fitur Utama
1. **Autentikasi Aman**: Login menggunakan hashing kata sandi satu arah **SHA-256** dan *parameterized queries* untuk mencegah SQL Injection.
2. **Otorisasi Berbasis Peran (RBAC)**:
   - **Admin (Petugas)**: Memiliki hak akses penuh untuk melihat, menambah (Create), memperbarui (Update), dan menghapus (Delete) data buku perpustakaan.
   - **Anggota (Mahasiswa)**: Memiliki hak akses terbatas hanya untuk melihat data koleksi buku (*read-only*). Tombol aksi Simpan, Update, dan Delete dikunci otomatis (`state="disabled"`).
3. **Manajemen Data Buku & Anggota**: Formulir interaktif yang terhubung langsung ke database MySQL.
4. **Fitur Logout**: Menutup jendela utama perpustakaan dan mengembalikan pengguna ke jendela login dengan aman.
5. **Continuous Integration (CI Pipeline)**: Pengujian otomatis (Unit Testing dengan `pytest`) dan pengecekan sintaks (*linting* dengan `flake8`) yang terintegrasi di GitHub Actions.

---

## Struktur Direktori (MVC)

Proyek ini dibangun dengan pola arsitektur **Model-View-Controller (MVC)**:

```text
modul 3/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml     # Konfigurasi CI GitHub Actions (Linting & Pytest)
├── config/
│   └── database.py             # Konfigurasi dan koneksi database MySQL
├── controllers/
│   ├── anggota_controller.py   # Logika kontrol antarmuka data anggota
│   ├── auth_controller.py      # Logika kontrol login, validasi & otorisasi
│   └── buku_controller.py      # Logika kontrol CRUD buku & pembatasan role
├── models/
│   ├── anggota_model.py        # Model query database tabel anggota
│   ├── buku_model.py           # Model query database tabel buku
│   └── user_model.py           # Model autentikasi & registrasi user (SHA-256)
├── views/
│   ├── anggota_view.py         # GUI tampilan data anggota (CustomTkinter)
│   ├── buku_view.py            # GUI tampilan utama form & tabel buku
│   └── login_view.py           # GUI tampilan form login pengguna
├── test/
│   ├── test_auth.py            # Unit test fungsi hashing & otentikasi
│   ├── test_authorization.py   # Unit test otorisasi role & tombol logout
│   ├── test_buku.py            # Unit test CRUD model buku
│   └── test_user.py            # Unit test registrasi dan user model
├── dist/
│   └── AplikasiPerpustakaan.exe # File executable aplikasi (Standalone)
├── main.py                     # Titik masuk (entry-point) utama aplikasi
├── main_anggota.py             # Titik masuk pengujian tampilan anggota
├── requirements.txt            # Daftar dependensi Python
├── AplikasiPerpustakaan.spec   # Spesifikasi build PyInstaller
└── README.md                   # Dokumentasi teknis proyek
```

---

## Panduan Instalasi & Konfigurasi Database MySQL

### 1. Prasyarat Sistem
- **Python**: Versi 3.11 atau lebih baru
- **Database Server**: Laragon atau XAMPP (MySQL Service aktif pada port 3306)
- **Git**: Terpasang di sistem

### 2. Konfigurasi Database MySQL
1. Jalankan layanan **MySQL** pada panel kontrol Laragon atau XAMPP.
2. Buat database baru bernama `perpustakaan`:
   ```sql
   CREATE DATABASE perpustakaan;
   USE perpustakaan;
   ```
3. Buat tabel-tabel pendukung:
   ```sql
   -- Tabel Pengguna (Users)
   CREATE TABLE users (
       id_user INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(255) NOT NULL,
       role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
   );

   -- Tabel Buku
   CREATE TABLE buku (
       id_buku INT AUTO_INCREMENT PRIMARY KEY,
       judul VARCHAR(255) NOT NULL,
       penulis VARCHAR(255) NOT NULL,
       tahun_terbit INT NOT NULL
   );

   -- Tabel Anggota
   CREATE TABLE anggota (
       id_anggota INT AUTO_INCREMENT PRIMARY KEY,
       nama VARCHAR(150) NOT NULL,
       alamat TEXT NOT NULL
   );
   ```

4. Masukkan data pengguna awal:
   ```sql
   -- Password: admin123 (hash SHA-256)
   INSERT INTO users (username, password, role) VALUES 
   ('petugas', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');

   -- Password: user123 (hash SHA-256)
   INSERT INTO users (username, password, role) VALUES 
   ('mahasiswa', 'e606e38b0d8c19b24cf0ee3808183162ea7cd63ff7912dbb22b5e803286b4446', 'anggota');
   ```

### 3. Konfigurasi Koneksi Aplikasi
Pengaturan koneksi tersimpan di file `config/database.py`:
- **Host**: `127.0.0.1` (atau `localhost`)
- **Port**: `3306`
- **Database**: `perpustakaan`
- **User**: `root`
- **Password**: *(kosong)*

---

## Cara Menjalankan Aplikasi

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/rizkialghifari2008-rgb/Modul3_RPL.git
   cd Modul3_RPL
   ```

2. **Membuat & Mengaktifkan Virtual Environment (Opsional tapi Direkomendasikan)**:
   ```bash
   python -m venv env
   # Windows:
   .\env\Scripts\activate
   # Linux/macOS:
   source env/bin/activate
   ```

3. **Instalasi Dependensi**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Menjalankan Aplikasi Utama**:
   ```bash
   python main.py
   ```

5. **Kredensial Login Bawaan**:
   | Role | Username | Password | Hak Akses |
   | :--- | :--- | :--- | :--- |
   | **Admin** | `petugas` | `admin123` | Akses penuh (Tambah, Ubah, Hapus, Lihat) |
   | **Anggota** | `mahasiswa` | `user123` | Akses terbatas (Hanya Lihat / Terkunci) |

---

## Pengujian Otomatis & Linting

### Menjalankan Unit Testing (Pytest)
```bash
python -m pytest -v
```

### Menjalankan Pengecekan Sintaks (Flake8)
```bash
flake8 models/ controllers/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

---

## Kompilasi Executable (.exe)

Untuk membuat file executable mandiri (*standalone* Windows `.exe`):
```bash
pyinstaller --clean -y AplikasiPerpustakaan.spec
```
File hasil build akan berada di direktori `dist/AplikasiPerpustakaan.exe`.
