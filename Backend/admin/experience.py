from flask import Blueprint, request, session, redirect, url_for, flash
from config import get_db_connection

experience_bp = Blueprint('experience', __name__)

@experience_bp.route('/admin/add-pengalaman', methods=['POST'])
def add_pengalaman():
    posisi = request.form['posisi']
    institusi = request.form['institusi']
    tahun = request.form['tahun']
    deskripsi = request.form['deskripsi']
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO pengalaman (posisi, institusi, tahun, deskripsi) VALUES (%s, %s, %s, %s)',
            (posisi, institusi, tahun, deskripsi)
        )
        conn.commit()
        conn.close()
        flash('Data pengalaman berhasil ditambahkan!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))

@experience_bp.route('/admin/delete-pengalaman/<int:id>')
def delete_pengalaman(id):
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pengalaman WHERE id = %s', (id,))
        conn.commit()
        conn.close()
        flash('Data pengalaman berhasil dihapus!', 'warning')
    return redirect(url_for('dashboard.admin_dashboard'))

@experience_bp.route('/admin/update-pengalaman/<int:id>', methods=['POST'])
def update_pengalaman(id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))
        
    posisi = request.form['posisi']
    institusi = request.form['institusi']
    tahun = request.form['tahun']
    deskripsi = request.form['deskripsi']
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pengalaman 
            SET posisi = %s, institusi = %s, tahun = %s, deskripsi = %s 
            WHERE id = %s
        ''', (posisi, institusi, tahun, deskripsi, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Riwayat pengalaman berhasil diperbarui! ✨', 'success')
    else:
        flash(f'Gagal terhubung ke database: {error}', 'danger')
        
    return redirect(url_for('dashboard.admin_dashboard'))