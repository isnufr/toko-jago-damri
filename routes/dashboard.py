from flask import Blueprint, render_template
from flask_login import login_required
from models import Barang, Transaksi

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Contoh data ringkasan statis sementara (idealnya query dari database)
    total_penjualan = 1250000
    total_transaksi = 42
    total_item = 128
    stok_menipis = Barang.query.filter(Barang.stok <= Barang.stok_min).count()
    
    barang_menipis = Barang.query.filter(Barang.stok <= Barang.stok_min).limit(5).all()

    return render_template('dashboard.html', 
                           total_penjualan=total_penjualan, 
                           total_transaksi=total_transaksi, 
                           total_item=total_item, 
                           stok_menipis=stok_menipis,
                           barang_menipis=barang_menipis)
