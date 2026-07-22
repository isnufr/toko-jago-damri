# 🏪 TOKO JAGO DAMRI — Rencana Aplikasi Web POS

> **Status:** Draf Perencanaan + Struktur Awal  
> **Target:** Aplikasi web kasir & inventaris untuk usaha toko kecil  
> **Akses:** HP / Tablet (Responsive, PWA-ready)  
> **Model Bisnis:** Transaksi tunai langsung, tanpa pelanggan & utang/piutang

---

## 📋 Daftar Fitur

- [ ] **Kasir / Point of Sale (POS)** — input transaksi jual-beli harian (cash & carry)
- [ ] **Manajemen Stok & Inventaris** — CRUD barang, stok masuk/keluar
- [ ] **Laporan Penjualan** — harian & bulanan, ringkasan omzet
- [ ] **Multi-user** — kasir & pemilik (role-based)
- [ ] **Printout Label Harga** — cetak nama barang + harga untuk pajangan di meja
- [ ] **Dashboard Ringkas** — ringkasan penjualan hari ini, stok menipis

---

## 🧱 Tech Stack

| Layer | Teknologi | Alasan |
|---|---|---|
| **Backend** | Python + Flask | Ringan, cocok untuk SQLite, mudah deploy di VPS Ubuntu |
| **Database** | SQLite | Tanpa install database server, satu file, simpel |
| **Frontend** | HTML + Tailwind CSS + Alpine.js | Ringan, mobile-first, tanpa build tools ribet |
| **Printout** | HTML `@media print` + `window.print()` | Print label langsung dari browser |
| **Auth** | Flask-Login + session | Simple session-based auth |
| **Deploy** | Gunicorn + Nginx di Ubuntu VPS (Colify) | Standar production Python |

---

## 🎨 Tema UI — Andalai.id Style (Putih + Oranye)

Berdasarkan website **andalai.id**, aplikasi akan mengusung tema:
- **Light theme** — background putih bersih
- **Warna primer: Oranye** sebagai aksen untuk tombol, link, highlight
- Desain simpel, modern, dan profesional

### Palet Warna

| Peran | Warna | Hex |
|---|---|---|
| **Primary** | Oranye | `#F97316` / `#EA580C` |
| **Primary Hover** | Oranye Tua | `#C2410C` |
| **Background** | Putih | `#FFFFFF` |
| **Background Alt** | Abu Sangat Muda | `#F9FAFB` |
| **Surface / Card** | Putih + Border Tipis | `#FFFFFF` + `border-gray-200` |
| **Text Primary** | Abu Gelap/Hitam | `#111827` |
| **Text Secondary** | Abu Sedang | `#6B7280` |
| **Success** | Hijau | `#10B981` |
| **Danger** | Merah | `#EF4444` |
| **Warning** | Kuning/Oranye Muda | `#F59E0B` |
| **Border** | Abu Muda | `#E5E7EB` |

### Typography
- Font: **Inter** (sans-serif) — bersih, modern, mudah dibaca
- Heading: bold, warna gelap (`#111827`)
- Body: regular, `#374151` atau `#6B7280`

### Gaya Visual
- Background putih bersih, lega
- Kartu (card) putih dengan border abu tipis + sudut agak melengkung (`rounded-lg` / `rounded-xl`)
- Tombol oranye dengan rounded (`rounded-lg` atau `rounded-full`)
- Shadow ringan (`shadow-sm` / `shadow`) untuk depth
- Ikon: **Lucide Icons** atau **Heroicons** (SVG)
- Spacing luas, layout bersih & minimalis
- Navbar sticky di atas (desktop) atau bottom navbar (mobile)

---

## 🗄️ Skema Database (SQLite)

### `users`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | |
| username | TEXT UNIQUE | |
| password_hash | TEXT | |
| role | TEXT | `owner` / `cashier` |
| nama_lengkap | TEXT | |
| created_at | TIMESTAMP | |

### `kategori`
| Kolom | Tipe |
|---|---|
| id | INTEGER PK |
| nama | TEXT UNIQUE |

### `barang`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | |
| kode | TEXT UNIQUE | Kode/PLU barang |
| nama | TEXT | |
| kategori_id | INTEGER FK | |
| harga_beli | INTEGER | |
| harga_jual | INTEGER | |
| stok | INTEGER | |
| stok_min | INTEGER | Alert jika stok ≤ ini |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### `transaksi`
| Kolom | Tipe | Keterangan |
|---|---|---|
| id | INTEGER PK | |
| no_invoice | TEXT UNIQUE | Format: `INV-YYYYMMDD-001` |
| user_id | INTEGER FK | Kasir yg input |
| total | INTEGER | |
| bayar | INTEGER | |
| kembalian | INTEGER | |
| created_at | TIMESTAMP | |

### `transaksi_detail`
| Kolom | Tipe |
|---|---|
| id | INTEGER PK |
| transaksi_id | INTEGER FK |
| barang_id | INTEGER FK |
| qty | INTEGER |
| harga_satuan | INTEGER |
| subtotal | INTEGER |

---

## 📁 Struktur Proyek

```
toko-jago-damri/
├── app.py                  # Flask entry point
├── config.py               # Konfigurasi
├── database.py             # Inisialisasi SQLite
├── models.py               # Model/query helper
├── requirements.txt        # Dependensi Python
├── seed.py                 # Seeder data awal
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Login/logout
│   ├── dashboard.py        # Dashboard
│   ├── barang.py           # CRUD barang
│   ├── transaksi.py        # POS & riwayat
│   ├── laporan.py          # Laporan
│   └── printout.py         # Print label harga
│
├── templates/
│   ├── base.html           # Layout utama
│   ├── login.html
│   ├── dashboard.html
│   ├── barang/
│   │   ├── index.html
│   │   ├── tambah.html
│   │   └── edit.html
│   ├── transaksi/
│   │   ├── pos.html        # Layar kasir
│   │   └── riwayat.html
│   ├── laporan/
│   │   ├── harian.html
│   │   └── bulanan.html
│   └── printout/
│       └── label.html      # Halaman print label
│
├── static/
│   ├── css/
│   │   └── tailwind.css
│   └── js/
│       └── app.js
│
└── deploy/
    ├── nginx.conf
    └── gunicorn.service
```

---

## 🖨️ Fitur Printout Label Harga

Fitur ini menggunakan CSS `@media print` agar saat user klik "Cetak Label", browser akan membuka jendela print dengan layout label yang rapi:

- Pilih barang yang ingin dicetak labelnya (checkbox)
- Atur jumlah copy per barang
- Preview tampilan label
- Klik **Cetak** → muncul dialog print browser
- Bisa pakai thermal printer (ukuran 58mm/80mm) atau printer A4

---

## 🚀 Langkah Awal Development

### 1. Setup Environment VPS Ubuntu (Colify)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx git -y

# Setup project
mkdir -p /var/www/toko-jago-damri
cd /var/www/toko-jago-damri
python3 -m venv venv
source venv/bin/activate
pip install flask flask-login gunicorn
```

### 2. Inisialisasi Database
```bash
python database.py   # Buat tabel
python seed.py       # Isi data contoh (admin + barang dummy)
```

### 3. Jalankan Development
```bash
flask run --host=0.0.0.0 --port=5000
```

### 4. Production (Gunicorn + Nginx)
```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
# + setup Nginx reverse proxy ke port 8000
```

---

## 📝 Catatan & Pertimbangan

- SQLite cocok untuk single-instance, traffic rendah-menengah. Jika nanti toko berkembang pesat, bisa migrasi ke PostgreSQL.
- Gunakan **Tailwind CSS via CDN** dulu untuk development cepat, nanti build production pakai CLI untuk ukuran file kecil.
- PWA bisa ditambahkan nanti agar bisa "install" di HP seperti aplikasi native.
- Backup database: cukup copy file `.db` secara berkala via cron job.

---

## ⏭️ Next: Kode Awal

Langkah selanjutnya — saya siap tuliskan kode awal:
1. `app.py` + `config.py` + `database.py` (kerangka Flask)
2. Template `base.html` dengan tema putih + oranye ala Andalai.id
3. Halaman login + dashboard awal
4. Modul barang (CRUD sederhana)

> 👉 **Ketik "LANJUT"** dan saya akan mulai tuliskan kode sumber lengkap tahap pertama!