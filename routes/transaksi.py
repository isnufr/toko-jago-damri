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

import uuid

@transaksi_bp.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.json
    cart = data.get('cart', [])
    total = data.get('total', 0)
    bayar = data.get('payment', 0)
    kembalian = data.get('change', 0)

    if not cart:
        return jsonify({'success': False, 'message': 'Keranjang kosong'}), 400

    # Buat invoice unik
    invoice_no = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:4].upper()}"

    transaksi = Transaksi(
        no_invoice=invoice_no,
        user_id=current_user.id,
        total=total,
        bayar=bayar,
        kembalian=kembalian
    )
    db.session.add(transaksi)
    db.session.flush() # Agar mendapatkan ID transaksi

    for item in cart:
        barang_id = item.get('id')
        qty = item.get('qty')
        harga_satuan = item.get('price')
        subtotal = item.get('subtotal')

        detail = TransaksiDetail(
            transaksi_id=transaksi.id,
            barang_id=barang_id,
            qty=qty,
            harga_satuan=harga_satuan,
            subtotal=subtotal
        )
        db.session.add(detail)

        # Potong stok barang
        barang = Barang.query.get(barang_id)
        if barang:
            barang.stok -= qty

    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Transaksi berhasil disimpan',
        'invoice': invoice_no,
        'transaksi_id': transaksi.id
    })

@transaksi_bp.route('/riwayat')
@login_required
def riwayat():
    # Mengambil transaksi terbaru, diurutkan dari yang paling baru
    daftar_transaksi = Transaksi.query.order_by(Transaksi.created_at.desc()).all()
    return render_template('transaksi/riwayat.html', riwayat=daftar_transaksi)

@transaksi_bp.route('/riwayat/<int:id>')
@login_required
def riwayat_detail(id):
    transaksi = Transaksi.query.get_or_404(id)
    return render_template('transaksi/detail.html', transaksi=transaksi)

from flask import flash, redirect, url_for

@transaksi_bp.route('/riwayat/hapus/<int:id>', methods=['POST'])
@login_required
def hapus_transaksi(id):
    transaksi = Transaksi.query.get_or_404(id)
    
    # Kembalikan stok barang
    for detail in transaksi.details:
        if detail.barang:
            detail.barang.stok += detail.qty
        db.session.delete(detail)
        
    db.session.delete(transaksi)
    db.session.commit()
    
    flash('Transaksi berhasil dihapus dan stok barang telah dikembalikan.', 'success')
    return redirect(url_for('transaksi.riwayat'))
