# WatchList API — Daftar Film Favorit

REST API untuk mengelola daftar film favorit menggunakan FastAPI dan Pydantic V2.

## Fitur
- Menambahkan film favorit
- Melihat seluruh daftar film
- Melihat detail film berdasarkan ID
- Memperbarui data film
- Menghapus film
- Validasi judul, genre, tahun rilis, dan rating
- Autentikasi menggunakan API Key
- Automated testing menggunakan pytest

## Teknologi
- Python
- FastAPI
- Pydantic V2
- Uvicorn
- Pytest
- HTTPX

## Instalasi

Buat virtual environment:

```powershell
python -m venv .venv
```

Aktifkan di PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instal dependensi:

```powershell
python -m pip install -r requirements.txt
```

## Menjalankan aplikasi

```powershell
uvicorn main:app --reload
```

Dokumentasi API tersedia di:

http://127.0.0.1:8000/docs

## Autentikasi

Gunakan header `X-API-Key` dengan nilai `watchlist-secret-key` untuk latihan lokal.

## Menjalankan pengujian

```powershell
python -m pytest -v
```

## Catatan

Data film disimpan sementara di memori. Data akan hilang ketika server dimulai ulang.
