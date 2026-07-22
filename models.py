from database import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='cashier') # owner / cashier
    nama_lengkap = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Kategori(db.Model):
    __tablename__ = 'kategori'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship
    barang_list = db.relationship('Barang', backref='kategori', lazy=True)

class Barang(db.Model):
    __tablename__ = 'barang'
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50), unique=True, nullable=False)
    nama = db.Column(db.String(150), nullable=False)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=True)
    harga_beli = db.Column(db.Integer, nullable=False, default=0)
    harga_jual = db.Column(db.Integer, nullable=False, default=0)
    stok = db.Column(db.Integer, nullable=False, default=0)
    stok_min = db.Column(db.Integer, nullable=False, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    id = db.Column(db.Integer, primary_key=True)
    no_invoice = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Integer, nullable=False, default=0)
    bayar = db.Column(db.Integer, nullable=False, default=0)
    kembalian = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    details = db.relationship('TransaksiDetail', backref='transaksi', lazy=True)
    kasir = db.relationship('User', backref='transaksi_list', lazy=True)

class TransaksiDetail(db.Model):
    __tablename__ = 'transaksi_detail'
    id = db.Column(db.Integer, primary_key=True)
    transaksi_id = db.Column(db.Integer, db.ForeignKey('transaksi.id'), nullable=False)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False, default=1)
    harga_satuan = db.Column(db.Integer, nullable=False, default=0)
    subtotal = db.Column(db.Integer, nullable=False, default=0)

    # Relationship
    barang = db.relationship('Barang', lazy=True)
