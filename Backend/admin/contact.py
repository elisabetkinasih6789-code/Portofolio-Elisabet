# File: Backend/admin/contact.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from config import get_db_connection
import resend

contact_bp = Blueprint('contact', __name__)

# ===================================================
# KONFIGURASI API KEY RESEND KAMU
# ===================================================
resend.api_key = "re_4s1aQheG_KDc4PD16noesQgDkaLt2kNCD" # <-- Pastikan diganti dengan API Key asli kamu ya

@contact_bp.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Paket data JSON kosong."}), 400

        nama = data.get('name')
        email = data.get('email')
        isi_pesan = data.get('message')

        # 1. JALUR SIMPAN KE DATABASE TiDB CLOUD
        conn, error = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO pesan (nama, email, isi_pesan, status) VALUES (%s, %s, %s, "belum dibaca")',
                (nama, email, isi_pesan)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("✓ [DEBUG] Sukses simpan ke TiDB Cloud!")
        else:
            return jsonify({"status": "error", "message": f"Gagal konek TiDB: {error}"}), 500

        # 2. JALUR KIRIM EMAIL VIA RESEND (DENGAN INTIP DATA)
        try:
            print(f"\n=== [DEBUG RESEND] MEMULAI PROSES EMAIL ===")
            print(f"API Key yang dibaca: {resend.api_key}")
            
            # Kita lepas kondisi if pengecek teks bawaan agar Resend dipaksa jalan mutlak
            print("Mengirim data ke Resend server...")
            resend.Emails.send({
                "from": "Portfolio Message <onboarding@resend.dev>",
                "to": "elisabetkinasih6789@gmail.com",
                "subject": f"✨ Pesan Baru dari {nama} (Portfolio)",
                "html": f"""
                    <h3>Ada pesan baru masuk!</h3>
                    <p><strong>Nama:</strong> {nama}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Pesan:</strong> {isi_pesan}</p>
                """
            })
            print("✓ [DEBUG RESEND] Server Resend sukses merespon tanpa eror!")

        except Exception as mail_err:
            # Jika baris Resend di atas eror, teks merah ini AKAN MUNCUL di terminal VS Code kamu
            print(f"❌ [DEBUG RESEND] PROSES GAGAL KARENA: {mail_err}")
            print("===========================================\n")

        return jsonify({"status": "success", "message": "Pesanmu berhasil terkirim!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Crash: {str(e)}"}), 500


# ===================================================
# FUNGSI YANG SEMPAT HILANG (Wajib Ada):
# ===================================================

@contact_bp.route('/admin/read-message/<int:id>')
def read_message(id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))

    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Mengubah status pesan menjadi sudah dibaca
        cursor.execute('UPDATE pesan SET status = "sudah dibaca" WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Pesan berhasil ditandai sebagai sudah dibaca! ✓', 'success')
    return redirect(url_for('dashboard.admin_dashboard'))


@contact_bp.route('/admin/delete-message/<int:id>')
def delete_message(id):
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))

    conn, error = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pesan WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Pesan masuk berhasil dihapus!', 'warning')
    return redirect(url_for('dashboard.admin_dashboard'))