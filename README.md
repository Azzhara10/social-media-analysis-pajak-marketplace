# Social Media Analysis: Pajak Marketplace

## Kelompok 7
# Dea Annisa Azzhara
# Nabila
# Kirana Ramadhani

## 1. Deskripsi Proyek
Proyek ini bertujuan mengumpulkan dan mengolah data dari media sosial X (Twitter) mengenai pajak marketplace. Topik ini dipilih karena berkaitan dengan bisnis digital, khususnya aktivitas jual beli melalui platform marketplace.

## 2. Sumber Data
- **Platform:** X (Twitter)
- **Topik:** Pajak marketplace
- **Kata kunci pencarian:** `pajak marketplace`
- **Rentang waktu:** 13 Juli–13 Oktober 2026
- **Metode scraping:** Tweet-Harvest

## 3. Proses Pengumpulan Data
Data dikumpulkan menggunakan Tweet-Harvest dengan kata kunci pencarian dan batas waktu yang telah ditentukan. Data hasil pengumpulan kemudian diolah menggunakan Python dan pandas untuk menyusun informasi ke dalam format CSV.

## 4. Struktur Data
Data terdiri dari enam kolom berikut:

| Kolom | Keterangan |
|---|---|
| `description` | Deskripsi atau teks informasi |
| `content` | Isi tweet |
| `title` | Judul jika tersedia |
| `timestamp` | Waktu publikasi dalam format Unix |
| `created at` | Tanggal dan waktu publikasi |
| `user` | Nama akun pengunggah |

## 5. File Output
File hasil pengolahan data:
- `pajak_marketplace_bersih.csv`

## 6. Tools yang Digunakan
- Tweet-Harvest
- Python
- pandas

## 7. Tujuan Analisis
Data ini dapat digunakan untuk mengamati percakapan di media sosial mengenai kebijakan pajak marketplace dan kaitannya dengan aktivitas bisnis digital.