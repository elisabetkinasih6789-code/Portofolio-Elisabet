# File: Backend/admin/hobbies.py
from flask import Blueprint, request, redirect, url_for, flash
from config import get_db_connection

hobbies_bp = Blueprint('hobbies_admin', __name__, url_prefix='/admin/hobbies')

# 1. READ: Dialihkan langsung ke dashboard utama karena boks hobbies.html 
# sudah bersatu padu di dalam sistem tab dashboard.html via {% include %}
@hobbies_bp.route('/')
def index():
    return redirect('/dashboard')

# 2. CREATE: Menambah hobi baru
@hobbies_bp.route('/add', methods=['POST'])
def add_hobby():
    nama_hobi = request.form.get('nama_hobi')
    icon = request.form.get('icon')
    deskripsi = request.form.get('deskripsi')
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO hobi (nama_hobi, icon, deskripsi) VALUES (%s, %s, %s)", 
                       (nama_hobi, icon, deskripsi))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Hobi baru berhasil ditambahkan!", "success")
        return redirect('/dashboard') # ◄── REVISI: Redirect langsung ke Dashboard Utama SPA
    return f"Database Error: {error}", 500

# 3. UPDATE: Mengedit hobi yang sudah ada via Modal Form
@hobbies_bp.route('/edit/<int:id>', methods=['POST'])
def edit_hobby(id):
    nama_hobi = request.form.get('nama_hobi')
    icon = request.form.get('icon')
    deskripsi = request.form.get('deskripsi')
    
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE hobi SET nama_hobi=%s, icon=%s, deskripsi=%s WHERE id=%s", 
                       (nama_hobi, icon, deskripsi, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Data hobi berhasil diperbarui!", "success")
        return redirect('/dashboard') # ◄── REVISI: Redirect langsung ke Dashboard Utama SPA
    return f"Database Error: {error}", 500

# 4. DELETE: Menghapus hobi secara permanen
@hobbies_bp.route('/delete/<int:id>', methods=['POST'])
def delete_hobby(id):
    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hobi WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Hobi berhasil dihapus dari portofolio!", "danger")
        return redirect('/dashboard') # ◄── REVISI: Redirect langsung ke Dashboard Utama SPA
    return f"Database Error: {error}", 500