-- ===================================================
-- BLUEPRINT DATABASE PORTOFOLIO ELISABET
-- ===================================================

CREATE DATABASE IF NOT EXISTS portofolio_db;
USE portofolio_db;

-- 1. TABEL PROFIL (Menyimpan Nama dan Bio Utamamu)
CREATE TABLE IF NOT EXISTS profil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    deskripsi TEXT NOT NULL
);

-- 2. TABEL PENGALAMAN (Kelola Experience)
CREATE TABLE IF NOT EXISTS pengalaman (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tahun VARCHAR(50) NOT NULL,
    posisi VARCHAR(100) NOT NULL,
    institusi VARCHAR(100) NOT NULL,
    deskripsi TEXT NOT NULL
);

-- 3. TABEL SKILL (Kelola Skills - Menggunakan nama 'skill' tanpa s)
CREATE TABLE IF NOT EXISTS skill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kategori VARCHAR(100) NOT NULL,
    nama_skill VARCHAR(100) NOT NULL
);

-- 4. TABEL PROYEK (Kelola Projects Portofolio)
CREATE TABLE IF NOT EXISTS proyek (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(150) NOT NULL,
    deskripsi TEXT NOT NULL,
    gambar_url VARCHAR(255) NULL,
    link_proyek VARCHAR(255) NULL
);

-- 5. TABEL HOBI (Kelola Hobi & Interests yang Kita Sinkronkan Kemarin)
CREATE TABLE IF NOT EXISTS hobi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_hobi VARCHAR(100) NOT NULL,
    icon VARCHAR(100) NOT NULL, -- Menyimpan class FontAwesome, misal: fa-solid fa-mug-hot
    deskripsi TEXT NOT NULL
);

-- 6. TABEL PESAN (Kotak Pesan Masuk Pengunjung - Kolom Harus Sesuai Aslinya)
CREATE TABLE IF NOT EXISTS pesan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    isi_pesan TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'belum dibaca',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- DATA AWAL (SEEDER) AGAR TIDAK UNDEFINED ERROR
-- ===================================================
INSERT INTO profil (nama, deskripsi) 
SELECT 'Elisabet Putri Kinasih', 'Mahasiswa Information Systems yang berfokus pada pengembangan sistem cerdas dan manajemen bisnis.'
WHERE NOT EXISTS (SELECT 1 FROM profil);