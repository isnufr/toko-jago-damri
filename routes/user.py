from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import User
from database import db

user_bp = Blueprint('user', __name__)

from functools import wraps

def owner_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.role != 'owner':
            abort(403)
        return f(*args, **kwargs)
    return wrapper

@user_bp.route('/users')
@login_required
@owner_required
def index():
    users = User.query.order_by(User.id).all()
    return render_template('users/index.html', users=users)

@user_bp.route('/users/tambah', methods=['GET', 'POST'])
@login_required
@owner_required
def tambah():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nama_lengkap = request.form.get('nama_lengkap')
        role = request.form.get('role')

        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan, silakan pilih yang lain.', 'error')
            return redirect(url_for('user.tambah'))

        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            nama_lengkap=nama_lengkap,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Pengguna baru berhasil ditambahkan.', 'success')
        return redirect(url_for('user.index'))

    return render_template('users/form.html', user=None)

@user_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@owner_required
def edit(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        username = request.form.get('username')
        
        # Cek duplikat username jika diubah
        if username != user.username and User.query.filter_by(username=username).first():
            flash('Username sudah digunakan, silakan pilih yang lain.', 'error')
            return redirect(url_for('user.edit', id=id))

        user.username = username
        user.nama_lengkap = request.form.get('nama_lengkap')
        user.role = request.form.get('role')
        
        # Update password hanya jika diisi
        password = request.form.get('password')
        if password and password.strip():
            user.password_hash = generate_password_hash(password)

        db.session.commit()
        flash('Data pengguna berhasil diperbarui.', 'success')
        return redirect(url_for('user.index'))

    return render_template('users/form.html', user=user)

@user_bp.route('/users/hapus/<int:id>', methods=['POST'])
@login_required
@owner_required
def hapus(id):
    user = User.query.get_or_404(id)
    
    # Mencegah owner terakhir atau diri sendiri dihapus
    if user.id == current_user.id:
        flash('Anda tidak dapat menghapus akun Anda sendiri.', 'error')
        return redirect(url_for('user.index'))
        
    owner_count = User.query.filter_by(role='owner').count()
    if user.role == 'owner' and owner_count <= 1:
        flash('Tidak dapat menghapus admin terakhir.', 'error')
        return redirect(url_for('user.index'))

    db.session.delete(user)
    db.session.commit()
    flash('Pengguna berhasil dihapus.', 'success')
    return redirect(url_for('user.index'))
