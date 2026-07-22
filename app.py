from flask import Flask
from config import Config
from database import db
from flask_login import LoginManager
from models import User

# Inisialisasi app Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inisialisasi Database
db.init_app(app)

# Inisialisasi LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrasi Blueprints (Routing)
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.barang import barang_bp
from routes.transaksi import transaksi_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(barang_bp)
app.register_blueprint(transaksi_bp)

# Inisialisasi database jika dijalankan secara langsung
with app.app_context():
    # Perintah pembuatan tabel otomatis jika belum ada bisa ditambahkan di sini, 
    # namun umumnya ditangani oleh seed.py atau flask-migrate
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
