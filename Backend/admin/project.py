# File: Backend/admin/project.py
from flask import Blueprint, request, session, redirect, url_for, flash
from config import get_db_connection

# IMPORT CLOUDINARY SDK
import cloudinary
import cloudinary.uploader

projects_bp = Blueprint('projects', __name__)

# ===================================================
# KONFIGURASI KREDENSIAL CLOUDINARY KAMU
# ===================================================
cloudinary.config(
    cloud_name = "dpiur9ybc",
    api_key = "272534332143256",
    api_secret = "e_zWN6kaa29mDpdMkIoVYjwqlPA",
    secure = True
)

@projects_bp.route('/admin/add-proyek', methods=['POST'])
def add_proyek():
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))
        
    judul = request.form['judul']
    link_proyek = request.form['link_proyek']
    deskripsi = request.form['deskripsi']
    
    # LOGIKA PROSES UPLOAD GAMBAR BARU KE CLOUDINARY
    gambar_url = ""
    if 'gambar' in request.files:
        file_gambar = request.files['gambar']
        if file_gambar.filename != '':
            upload_result = cloudinary.uploader.upload(file_gambar, folder="portfolio_elisabet")
            gambar_url = upload_result['secure_url']

    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO proyek (judul, gambar_url, link_proyek, deskripsi) VALUES (%s, %s, %s, %s)', 
                       (judul, gambar_url, link_proyek, deskripsi))
        conn.commit()
        conn.close()
        flash('Proyek baru beserta gambar berhasil disimpan!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))


@projects_bp.route('/admin/update-proyek/<int:id>', methods=['POST'])
def update_proyek(id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))
        
    judul = request.form['judul']
    link_proyek = request.form['link_proyek']
    deskripsi = request.form['deskripsi']
    gambar_url_lama = request.form['gambar_url_lama']
    
    # LOGIKA EDIT GAMBAR
    gambar_url = gambar_url_lama
    if 'gambar' in request.files:
        file_gambar = request.files['gambar']
        if file_gambar.filename != '':
            upload_result = cloudinary.uploader.upload(file_gambar, folder="portfolio_elisabet")
            gambar_url = upload_result['secure_url']

    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE proyek 
            SET judul = %s, gambar_url = %s, link_proyek = %s, deskripsi = %s 
            WHERE id = %s
        ''', (judul, gambar_url, link_proyek, deskripsi, id))
        conn.commit()
        conn.close()
        flash('Data proyek berhasil diperbarui! ✨', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))


# ===================================================
# BAGIAN YANG KELUPAAN KEMARIN: RUTE HAPUS DATA PROYEK
# ===================================================
@projects_bp.route('/admin/delete-proyek/<int:id>')
def delete_proyek(id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))
        
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Menghapus baris karya dari tabel proyek berdasarkan ID-nya
        cursor.execute('DELETE FROM proyek WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proyek berhasil dihapus dari portofolio!', 'warning')
    else:
        flash(f'Gagal terhubung ke database: {error}', 'danger')
        
    return redirect(url_for('dashboard.admin_dashboard'))