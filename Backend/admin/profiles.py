from flask import Blueprint, request, redirect, url_for, flash
from config import get_db_connection

profiles_bp = Blueprint('profiles', __name__)

@profiles_bp.route('/admin/update-profil', methods=['POST'])
def update_profil():
    nama = request.form['nama']
    deskripsi = request.form['deskripsi']
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE profil SET nama = %s, deskripsi = %s WHERE id = 1', (nama, deskripsi))
        conn.commit()
        conn.close()
        flash('Profil Utama & About Me berhasil diperbarui!', 'success')
    else:
        flash(f'Gagal memperbarui database: {error}', 'danger')
    return redirect(url_for('dashboard.admin_dashboard'))