# File: Backend/admin/skills.py
from flask import Blueprint, request, session, redirect, url_for, flash
from config import get_db_connection

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/admin/add-skill', methods=['POST'])
def add_skill():
    nama_skill = request.form['nama_skill']
    kategori = request.form['kategori']
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO skill (nama_skill, kategori) VALUES (%s, %s)', (nama_skill, kategori))
        conn.commit()
        conn.close()
        flash('Skill baru berhasil ditambahkan!', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))

@skills_bp.route('/admin/delete-skill/<int:id>')
def delete_skill(id):
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM skill WHERE id = %s', (id,))
        conn.commit()
        conn.close()
        flash('Skill berhasil dihapus!', 'warning')
    return redirect(url_for('dashboard.admin_dashboard'))

@skills_bp.route('/admin/update-skill/<int:id>', methods=['POST'])
def update_skill(id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))
        
    nama_skill = request.form['nama_skill']
    kategori = request.form['kategori']
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # SUDAH DIPERBAIKI: 'skills' diganti menjadi 'skill'
        cursor.execute('UPDATE skill SET nama_skill = %s, kategori = %s WHERE id = %s', (nama_skill, kategori, id))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash('Keahlian berhasil diperbarui! ✨', 'success')
    else:
        flash(f'Gagal memperbarui database: {error}', 'danger')
        
    return redirect(url_for('dashboard.admin_dashboard'))