from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import Barang, Transaksi, TransaksiDetail
from database import db
from datetime import datetime

transaksi_bp = Blueprint('transaksi', __name__)

@transaksi_bp.route('/pos')
@login_required
def pos():
    return render_template('transaksi/pos.html')

@transaksi_bp.route('/api/barang')
@login_required
def api_barang():
    barang = Barang.query.all()
    # Mengubah data barang menjadi format JSON (list of dict) untuk di-load oleh Alpine.js
    hasil = []
    for b in barang:
        hasil.append({
            'id': b.id,
            'sku': b.kode,
            'name': b.nama,
            'price': b.harga_jual,
            'stock': b.stok
        })
    return jsonify(hasil)

# Placeholder untuk route riwayat
@transaksi_bp.route('/riwayat')
@login_required
def riwayat():
    return "Halaman Riwayat Transaksi"
