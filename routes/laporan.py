from flask import Blueprint, render_template, request
from flask_login import login_required
from models import Transaksi
from database import db
from sqlalchemy import extract, func
from datetime import datetime

laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')

@laporan_bp.route('/')
@login_required
def index():
    # Ambil filter tahun, default tahun ini
    tahun_aktif = request.args.get('tahun', datetime.now().year, type=int)
    
    # Ambil list tahun unik dari transaksi (untuk dropdown filter)
    # Di SQLite extract() kadang rewel, pakai strftime
    # func.strftime('%Y', Transaksi.created_at)
    semua_transaksi = Transaksi.query.all()
    tahun_tersedia = sorted(list(set([t.created_at.year for t in semua_transaksi])))
    if not tahun_tersedia:
        tahun_tersedia = [tahun_aktif]
    elif tahun_aktif not in tahun_tersedia:
        tahun_tersedia.append(tahun_aktif)
        tahun_tersedia.sort()

    # Hitung laporan per bulan (1 - 12)
    laporan_bulanan = []
    total_tahunan = 0
    total_transaksi_tahunan = 0
    
    for bulan in range(1, 13):
        # Query total dan hitung transaksi di bulan & tahun tertentu
        # Karena strftime('%m') me-return '01', kita bisa filter manual di python 
        # atau query yang aman untuk lintas database
        trx_bulan_ini = [t for t in semua_transaksi if t.created_at.year == tahun_aktif and t.created_at.month == bulan]
        
        jml_transaksi = len(trx_bulan_ini)
        total_pendapatan = sum(t.total for t in trx_bulan_ini)
        pajak = int(total_pendapatan * 0.11) # Asumsi PPN 11%
        pendapatan_bersih = total_pendapatan - pajak
        
        laporan_bulanan.append({
            'bulan': bulan,
            'nama_bulan': get_nama_bulan(bulan),
            'jml_transaksi': jml_transaksi,
            'total_kotor': total_pendapatan,
            'pajak': pajak,
            'total_bersih': pendapatan_bersih
        })
        
        total_tahunan += total_pendapatan
        total_transaksi_tahunan += jml_transaksi

    pajak_tahunan = int(total_tahunan * 0.11)
    
    return render_template('laporan/index.html', 
                           tahun_aktif=tahun_aktif,
                           tahun_tersedia=tahun_tersedia,
                           laporan_bulanan=laporan_bulanan,
                           total_tahunan=total_tahunan,
                           total_transaksi_tahunan=total_transaksi_tahunan,
                           pajak_tahunan=pajak_tahunan)

def get_nama_bulan(angka):
    bulan = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    return bulan.get(angka, '')
