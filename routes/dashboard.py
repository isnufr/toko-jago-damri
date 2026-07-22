from flask import Blueprint, render_template
from flask_login import login_required
from models import Barang, Transaksi
from database import db
from sqlalchemy import func
from datetime import datetime, date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Hitung batas waktu mulai hari ini (jam 00:00:00)
    today_start = datetime.combine(date.today(), datetime.min.time())
    
    # Hitung total transaksi hari ini
    total_transaksi = Transaksi.query.filter(Transaksi.created_at >= today_start).count()
    
    # Hitung total pendapatan hari ini
    penjualan_hari_ini = db.session.query(func.sum(Transaksi.total)).filter(Transaksi.created_at >= today_start).scalar()
    total_penjualan = penjualan_hari_ini if penjualan_hari_ini else 0
    
    # Total jenis item barang yang terdaftar
    total_item = Barang.query.count()
    
    # Stok menipis
    stok_menipis = Barang.query.filter(Barang.stok <= Barang.stok_min).count()
    barang_menipis = Barang.query.filter(Barang.stok <= Barang.stok_min).limit(5).all()

    # Peringatan Kadaluarsa (< 30 hari & sudah lewat)
    batas_waktu_kadaluarsa = date.today() + timedelta(days=30)
    barang_kadaluarsa = Barang.query.filter(
        Barang.expired_date != None, 
        Barang.expired_date <= batas_waktu_kadaluarsa
    ).order_by(Barang.expired_date.asc()).all()
    jumlah_kadaluarsa = len(barang_kadaluarsa)

    return render_template('dashboard.html', 
                           total_penjualan=total_penjualan, 
                           total_transaksi=total_transaksi, 
                           total_item=total_item, 
                           stok_menipis=stok_menipis,
                           barang_menipis=barang_menipis,
                           barang_kadaluarsa=barang_kadaluarsa,
                           jumlah_kadaluarsa=jumlah_kadaluarsa)

