# File: Backend/admin/dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from config import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()

        # 1. Ambil Profil
        cursor.execute("SELECT nama, deskripsi FROM profil LIMIT 1")
        profil_data = cursor.fetchone()
        profil = {"nama": profil_data[0], "deskripsi": profil_data[1]} if profil_data else {"nama": "Elisabet", "deskripsi": ""}

        # 2. Ambil data Pengalaman
        cursor.execute("SELECT id, tahun, posisi, institusi, deskripsi FROM pengalaman")
        pengalaman_list = [{"id": r[0], "tahun": r[1], "posisi": r[2], "institusi": r[3], "deskripsi": r[4]} for r in cursor.fetchall()]

        # 3. Ambil data Skill
        cursor.execute("SELECT id, kategori, nama_skill FROM skill")
        skill_list = [{"id": r[0], "kategori": r[1], "nama_skill": r[2]} for r in cursor.fetchall()]

        # 4. Ambil data Proyek
        cursor.execute("SELECT id, judul, deskripsi, gambar_url, link_proyek FROM proyek")
        proyek_list = [{"id": r[0], "judul": r[1], "deskripsi": r[2], "gambar_url": r[3], "link_proyek": r[4]} for r in cursor.fetchall()]

        # 5. Ambil data Hobi
        cursor.execute("SELECT id, nama_hobi, icon, deskripsi FROM hobi")
        hobi_list = [{"id": r[0], "nama_hobi": r[1], "icon": r[2], "deskripsi": r[3]} for r in cursor.fetchall()]

        # 6. ──► PERBAIKAN AKURAT: KEMBALIKAN QUERY SESUAI KOLOM ASLI DATABASE ELISABET ◄──
        try:
            # Mengambil kolom isi_pesan, status, dan created_at sesuai kebutuhan messages.html
            cursor.execute("SELECT id, nama, email, isi_pesan, status, created_at FROM pesan ORDER BY id DESC")
            pesan_list = [
                {
                    "id": r[0], 
                    "nama": r[1], 
                    "email": r[2], 
                    "isi_pesan": r[3], 
                    "status": r[4], 
                    "created_at": r[5]
                } for r in cursor.fetchall()
            ]
        except Exception as e:
            # Jika ada eror tak terduga, detailnya akan dimunculkan ke terminal VS Code kamu
            print("\n🚨 ADA MASALAH DATABASE:", str(e), "\n")
            pesan_list = []

        cursor.close()
        conn.close()

        return render_template('dashboard.html',
                               profil=profil,
                               pengalaman_list=pengalaman_list,
                               skill_list=skill_list,
                               proyek_list=proyek_list,
                               hobi_list=hobi_list,
                               pesan_list=pesan_list)
    
    return f"Database Error: {error}", 500