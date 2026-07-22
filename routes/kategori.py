from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Kategori
from database import db

kategori_bp = Blueprint('kategori', __name__)

@kategori_bp.route('/kategori')
@login_required
def index():
    kategori_list = Kategori.query.all()
    return render_template('kategori/index.html', kategori_list=kategori_list)

@kategori_bp.route('/kategori/tambah', methods=['POST'])
@login_required
def tambah():
    nama = request.form.get('nama')
    if nama:
        # Cek apakah sudah ada
        existing = Kategori.query.filter_by(nama=nama).first()
        if existing:
            flash(f'Kategori "{nama}" sudah ada!', 'error')
        else:
            kategori_baru = Kategori(nama=nama)
            db.session.add(kategori_baru)
            db.session.commit()
            flash('Kategori berhasil ditambahkan', 'success')
    return redirect(url_for('kategori.index'))

@kategori_bp.route('/kategori/hapus/<int:id>', methods=['POST'])
@login_required
def hapus(id):
    kategori = Kategori.query.get_or_404(id)
    # Cek apakah kategori sedang digunakan oleh barang
    if kategori.barang_list:
        flash(f'Gagal menghapus! Kategori "{kategori.nama}" sedang digunakan oleh beberapa barang.', 'error')
    else:
        db.session.delete(kategori)
        db.session.commit()
        flash('Kategori berhasil dihapus', 'success')
    return redirect(url_for('kategori.index'))
