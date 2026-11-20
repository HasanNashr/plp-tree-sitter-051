# CLI Pendeteksi TODO, Fungsi Panjang, dan Syntax Error (`cek.py`)

Program baris perintah (CLI) berbasis **Tree-sitter** untuk memindai seluruh berkas Python (`.py`) di dalam suatu direktori dan mendeteksi potensi masalah kualitas kode secara deterministik.

## Fitur
1. **Deteksi Komentar `TODO` / `FIXME`**: Mencari komentar yang mengandung kata kunci `TODO` atau `FIXME` menggunakan Tree-sitter Query (`#match?`).
2. **Deteksi Fungsi Panjang (> 30 Baris)**: Menghitung rentang baris (`end_point[0] - start_point[0] + 1`) pada setiap `function_definition` (termasuk method di dalam kelas dan fungsi bersarang).
3. **Deteksi Syntax Error**: Memeriksa `root_node.has_error` dan menelusuri pohon secara rekursif untuk melaporkan baris dan kolom node `ERROR` atau `MISSING` pertama.

## Instalasi Dependensi
Pastikan Python 3.10+ sudah terpasang, lalu instal pustaka yang dibutuhkan:

```bash
pip install tree-sitter tree-sitter-python