# Menggunakan image Python versi slim agar ukurannya lebih kecil
FROM python:3.11-slim

# Mencegah Python membuat file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Memastikan log dari Python langsung tampil di terminal/stdout
ENV PYTHONUNBUFFERED=1

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Menginstal dependensi sistem yang mungkin diperlukan (contoh untuk build SQLite/C extensions)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Menyalin file requirements.txt terlebih dahulu
COPY requirements.txt .

# Menginstal dependensi Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek ke dalam container
COPY . .

# Membuat direktori untuk database SQLite jika belum ada, dan mengatur izin aksesnya
RUN mkdir -p /app/data && chmod -R 777 /app/data
ENV DATABASE_PATH=/app/data/toko_jago_damri.db

# Membuka port yang akan digunakan oleh aplikasi
EXPOSE 8000

# Menjalankan script seeder terlebih dahulu untuk setup database, lalu jalankan aplikasi dengan Gunicorn
CMD bash -c "python seed.py && gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app"
