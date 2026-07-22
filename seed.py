import os
from werkzeug.security import generate_password_hash
from app import app
from database import db
from models import User, Kategori, Barang

def seed_data():
    with app.app_context():
        print("Mereset tabel database...")
        db.drop_all()
        db.create_all()

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

        print("Menambahkan barang dummy...")
        # Sembako
        b1 = Barang(kode='8999999012345', nama='Minyak Goreng Bimoli 2L', kategori_id=kat_sembako.id, harga_beli=30000, harga_jual=35000, stok=12, stok_min=5)
        b2 = Barang(kode='BRG0001', nama='Beras Rojolele 5kg', kategori_id=kat_sembako.id, harga_beli=65000, harga_jual=75000, stok=15, stok_min=10)
        b3 = Barang(kode='8990987654321', nama='Gula Pasir Gulaku 1kg', kategori_id=kat_sembako.id, harga_beli=14000, harga_jual=16500, stok=4, stok_min=10)
        
        # Minuman / Snack
        b4 = Barang(kode='8991234567890', nama='Indomie Goreng', kategori_id=kat_snack.id, harga_beli=2500, harga_jual=3000, stok=45, stok_min=40)
        b5 = Barang(kode='8993216549870', nama='Teh Celup Sosro', kategori_id=kat_minuman.id, harga_beli=5000, harga_jual=6500, stok=25, stok_min=10)
        
        db.session.add_all([b1, b2, b3, b4, b5])
        db.session.commit()
        print("Data awal (seeder) berhasil ditambahkan!")

if __name__ == '__main__':
    seed_data()
