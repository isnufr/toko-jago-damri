import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-yang-sangat-aman-123'
    # Menggunakan path dari env variable (jika di docker) atau path lokal (jika di lokal)
    db_path = os.environ.get('DATABASE_PATH') or os.path.join(os.path.abspath(os.path.dirname(__file__)), 'toko_jago_damri.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
