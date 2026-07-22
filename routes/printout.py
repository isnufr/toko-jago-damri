from flask import Blueprint, render_template, request
from flask_login import login_required
from models import Barang

printout_bp = Blueprint('printout', __name__, url_prefix='/printout')

@printout_bp.route('/label')
@login_required
def label():
    # Mengambil semua barang untuk dipilih mana yang mau dicetak
    # atau bisa juga dengan menerima parameter ID barang tertentu
    barang_list = Barang.query.order_by(Barang.nama.asc()).all()
    return render_template('printout/label.html', barang_list=barang_list)
