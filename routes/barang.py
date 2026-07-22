from flask import Blueprint, render_template
from flask_login import login_required
from models import Barang

barang_bp = Blueprint('barang', __name__)

@barang_bp.route('/barang')
@login_required
def index():
    semua_barang = Barang.query.all()
    return render_template('barang/index.html', list_barang=semua_barang)

@barang_bp.route('/barang/tambah')
@login_required
def tambah():
    # Untuk sementara, route ini bisa diarahkan ke fungsi placeholder 
    # karena template HTML tambah belum dibuat secara utuh di tahap awal.
    return "Halaman Tambah Barang"

@barang_bp.route('/barang/edit/<int:id>')
@login_required
def edit(id):
    # Placeholder
    return f"Halaman Edit Barang ID: {id}"
