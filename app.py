# File: app.py (Di folder paling luar proyek)
from flask import Flask
from config import get_db_connection, SECRET_KEY
import os

# === IMPORT SELURUH BLUEPRINT MODULAR ===
from Backend.utama.utama import utama_bp
from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.experience import experience_bp
from Backend.admin.skills import skills_bp
from Backend.admin.project import projects_bp
from Backend.admin.upload import upload_bp
from Backend.admin.contact import contact_bp
# 1. DI SINI TEMPAT IMPORT HOBI BARU:
from Backend.admin.hobbies import hobbies_bp

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(base_dir, "Frontend"), 
            static_folder=os.path.join(base_dir, "Frontend"))
app.secret_key = SECRET_KEY

# === REGISTRASI SELURUH BLUEPRINT KE FLASK SYSTEM ===
app.register_blueprint(utama_bp)
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(experience_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(contact_bp)
# 2. DI SINI TEMPAT REGISTRASI HOBI BARU:
app.register_blueprint(hobbies_bp)

if __name__ == '__main__':
    # Sekarang di bawah ini sudah bersih tanpa ada sisa teks typo lagi
    app.run(debug=True, port=5001)