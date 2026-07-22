from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Barang, Kategori
from database import db

barang_bp = Blueprint('barang', __name__)

@barang_bp.route('/barang')
@login_required
def index():
    q = request.args.get('q', '')
    kat_id = request.args.get('kategori', '')
    page = request.args.get('page', 1, type=int)

    query = Barang.query
    if q:
        query = query.filter((Barang.nama.ilike(f'%{q}%')) | (Barang.kode.ilike(f'%{q}%')))
    if kat_id:
        query = query.filter(Barang.kategori_id == kat_id)
        
    query = query.order_by(Barang.nama.asc())
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    
    kategori_list = Kategori.query.all()
    
    return render_template('barang/index.html', pagination=pagination, q=q, kat_id=kat_id, kategori_list=kategori_list)

@barang_bp.route('/barang/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        kode = request.form.get('kode')
        nama = request.form.get('nama')
        kategori_id = request.form.get('kategori_id')
        harga_beli = request.form.get('harga_beli', type=int)
        harga_jual = request.form.get('harga_jual', type=int)
        stok = request.form.get('stok', type=int)
        stok_min = request.form.get('stok_min', type=int)

        # Cek kode unik
        if Barang.query.filter_by(kode=kode).first():
            flash(f'Kode Barang/PLU {kode} sudah digunakan.', 'error')
            return redirect(url_for('barang.tambah'))

        barang_baru = Barang(
            kode=kode, nama=nama, kategori_id=kategori_id,
            harga_beli=harga_beli, harga_jual=harga_jual,
            stok=stok, stok_min=stok_min
        )
        db.session.add(barang_baru)
        db.session.commit()
        flash('Data barang berhasil ditambahkan.', 'success')
        return redirect(url_for('barang.index'))

    kategori_list = Kategori.query.all()
    return render_template('barang/form.html', kategori_list=kategori_list, barang=None)

@barang_bp.route('/barang/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    barang = Barang.query.get_or_404(id)
    if request.method == 'POST':
        kode_baru = request.form.get('kode')
        # Cek jika kode diganti tapi bentrok dengan kode lain
        if kode_baru != barang.kode and Barang.query.filter_by(kode=kode_baru).first():
            flash(f'Kode Barang/PLU {kode_baru} sudah digunakan.', 'error')
            return redirect(url_for('barang.edit', id=id))

        barang.kode = kode_baru
        barang.nama = request.form.get('nama')
        barang.kategori_id = request.form.get('kategori_id')
        barang.harga_beli = request.form.get('harga_beli', type=int)
        barang.harga_jual = request.form.get('harga_jual', type=int)
        barang.stok = request.form.get('stok', type=int)
        barang.stok_min = request.form.get('stok_min', type=int)

        db.session.commit()
        flash('Data barang berhasil diperbarui.', 'success')
        return redirect(url_for('barang.index'))

    kategori_list = Kategori.query.all()
    return render_template('barang/form.html', kategori_list=kategori_list, barang=barang)

@barang_bp.route('/barang/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    barang = Barang.query.get_or_404(id)
    db.session.delete(barang)
    db.session.commit()
    flash('Data barang berhasil dihapus.', 'success')
    return redirect(url_for('barang.index'))
