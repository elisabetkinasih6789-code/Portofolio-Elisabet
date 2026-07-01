from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import get_db_connection

# Inisialisasi Blueprint untuk Login
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # SISTEM AUTO-REDIRECT SUDAH DIHAPUS
    # Sekarang, setiap rute /login dibuka, Flask akan SELALU meminta input username & password
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn, error = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            conn.close()
            
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('dashboard.admin_dashboard'))
            else:
                flash('Username atau Password salah!', 'danger')
        else:
            flash(f'Gagal terhubung ke database: {error}', 'danger')
            
    return render_template('login.html')

# File: Backend/admin/login.py

@login_bp.route('/logout')
def logout():
    session.clear() # Menghapus sesi login admin agar aman
    flash("Anda telah berhasil keluar.", "success")
    
    # ──► PERBAIKAN UTAMA: Alihkan ke halaman utama portofolio depan, bukan login!
    return redirect('/')