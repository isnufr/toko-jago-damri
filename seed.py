import os
from werkzeug.security import generate_password_hash
from app import app
from database import db
from models import User, Kategori, Barang

def seed_data():
    with app.app_context():
        print("Memeriksa struktur database...")
        db.create_all()

        # Cek apakah sudah ada user (admin/kasir) di database, jika ada berarti sudah pernah disetup
        if User.query.first():
            print("Database sudah berisi data pengguna, melewati proses reset awal.")
            return

        print("Menambahkan data admin awal...")
        # Tambah Admin
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='owner',
            nama_lengkap='Administrator'
        )
        db.session.add(admin)
        
        # Tambah Kasir dummy
        kasir = User(
            username='kasir',
            password_hash=generate_password_hash('kasir123'),
            role='cashier',
            nama_lengkap='Kasir Satu'
        )
        db.session.add(kasir)

        print("Menambahkan kategori...")
        kat_sembako = Kategori(nama='Sembako')
        kat_minuman = Kategori(nama='Minuman')
        kat_snack = Kategori(nama='Snack')
        db.session.add_all([kat_sembako, kat_minuman, kat_snack])
        db.session.commit()

        db.session.commit()
        print("Data awal (seeder) berhasil ditambahkan!")

if __name__ == '__main__':
    seed_data()
