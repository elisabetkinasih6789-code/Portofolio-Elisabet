# File: Backend/utama/utama.py
from flask import Blueprint, render_template
from config import get_db_connection

# Inisialisasi Blueprint untuk halaman utama
utama_bp = Blueprint('utama', __name__)

@utama_bp.route('/')
def index():
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM profil WHERE id = 1')
        profil = cursor.fetchone()
        
        cursor.execute('SELECT * FROM pengalaman ORDER BY id DESC')
        pengalaman_list = cursor.fetchall()
        
        cursor.execute('SELECT * FROM skill ORDER BY kategori DESC')
        skill_list = cursor.fetchall()
        
        cursor.execute('SELECT * FROM proyek ORDER BY id DESC')
        proyek_list = cursor.fetchall()
        
        conn.close()
        
        if not profil:
            profil = {'nama': 'Elisabet Putri Kinasih', 'deskripsi': 'SISP Student'}
            
        return render_template('utama/index.html', 
                               profil=profil, 
                               pengalaman_list=pengalaman_list, 
                               skill_list=skill_list, 
                               proyek_list=proyek_list)
    else:
        return f"Error Database: {error}"

# File: Backend/utama/utama.py
from flask import Blueprint, render_template
from config import get_db_connection

utama_bp = Blueprint('utama', __name__)

@utama_bp.route('/')
def index():
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # 1. Ambil data profil
        cursor.execute("SELECT nama, deskripsi FROM profil LIMIT 1")
        profil_data = cursor.fetchone()
        profil = {"nama": profil_data[0], "deskripsi": profil_data[1]} if profil_data else {"nama": "Elisabet", "deskripsi": ""}
        
        # 2. Ambil data skills
        cursor.execute("SELECT kategori, nama_skill FROM skill")
        skill_list = [{"kategori": r[0], "nama_skill": r[1]} for r in cursor.fetchall()]
        
        # 3. Ambil data pengalaman
        cursor.execute("SELECT tahun, posisi, institusi, deskripsi FROM pengalaman")
        pengalaman_list = [{"tahun": r[0], "posisi": r[1], "institusi": r[2], "deskripsi": r[3]} for r in cursor.fetchall()]
        
        # 4. Ambil data proyek
        cursor.execute("SELECT judul, deskripsi, gambar_url, link_proyek FROM proyek")
        proyek_list = [{"judul": r[0], "deskripsi": r[1], "gambar_url": r[2], "link_proyek": r[3]} for r in cursor.fetchall()]
        
        # 5. QUERY BARU: Ambil data dari tabel hobi
        cursor.execute("SELECT nama_hobi, icon, deskripsi FROM hobi")
        hobi_list = [{"nama_hobi": r[0], "icon": r[1], "deskripsi": r[2]} for r in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        # Mengirimkan semua data termasuk hobi_list ke HTML
        return render_template('utama/index.html', 
                               profil=profil, 
                               skill_list=skill_list, 
                               pengalaman_list=pengalaman_list, 
                               proyek_list=proyek_list,
                               hobi_list=hobi_list)
    else:
        return f"Database Error: {error}", 500