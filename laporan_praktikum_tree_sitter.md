# Eksplorasi Concrete Syntax Tree, Query, dan Grammar dengan Tree-sitter

**Laporan Praktikum & Tugas Awal — Sarjana Terapan Teknik Informatika**

| Keterangan | Detail |
| :--- | :--- |
| **Nama / Kelas** | Hasan Nashrullah — Kelas 2B (JTK) |
| **Repositori Proyek** | https://github.com/HasanNashr/plp-tree-sitter-051 |
| **Lingkungan Kerja** | Windows Native, Python 3.10+ (`tree-sitter`, `tree-sitter-python`), Node.js v24.14.1, `tree-sitter-cli` |

---

## 1. Ringkasan Pelaksanaan & Hasil Tugas 1–3 (`tugas1-3/`)

### Tugas 1 — Membaca Pohon Sintaks (`t1.py` & `hasil_t1.txt`)
Pengujian dilakukan pada tiga konstruksi kode Python (fungsi `sapa`, percabangan `if/else`, dan kelas `Mahasiswa`) dengan membandingkan pohon perkiraan tulisan tangan terhadap keluaran S-expression aktual. Pada definisi fungsi, node bernama mencakup `function_definition`, `identifier`, `parameters`, dan `return_statement`, sedangkan token seperti `'def'`, `':'`, `'('`, dan `')'` tersimpan sebagai node anonim (`is_named == False`). Saat tanda titik dua dihapus pada `def sapa(nama)`, parser tetap membentuk pohon dengan menyisipkan node `ERROR` sebagai bukti mekanisme *error recovery*.

**Inti Keluaran Terminal (`python t1.py`):**
```text
[Tempelkan 10-15 baris inti output S-expression, perbandingan named vs anonim, dan node ERROR dari t1.py di sini]
```

### Tugas 2 — Penjelajah Node Rekursif (`jelajah.py` & `hasil_t2.txt`)
Skrip `jelajah.py` menerapkan traversal preorder (DFS) dengan menelusuri `enumerate(node.children)` agar indeks anak sesuai saat memanggil `node.field_name_for_child(i)`, sambil menyaring node anonim menggunakan `child.is_named`. Program diuji bertahap dari berkas satu baris hingga `uji_100_baris.py` (127 baris kode manajemen tugas kuliah) dan menghasilkan struktur indentasi bertingkat lengkap dengan koordinat `[baris:kolom]` serta label `field:`.

**Inti Keluaran Terminal (`python jelajah.py uji_100_baris.py`):**
```text
[Tempelkan 10-15 baris pertama output traversal yang menampilkan indentasi, [baris:kolom], dan label field di sini]
```

### Tugas 3 — Pattern Matching dengan Query (`q.py` & berkas `.scm`)
Empat berkas query dieksekusi terhadap `uji_100_baris.py` menggunakan `QueryCursor.matches()` dan hasilnya dicocokkan dengan perhitungan manual baris demi baris:

| Berkas Query | Target Pola Sintaks | Hasil Program & Verifikasi Manual |
| :--- | :--- | :--- |
| `fungsi.scm` | `function_definition` beserta jumlah parameter | 9 fungsi ditemukan (`__init__`: 3 param hingga `jalankan_simulasi`: 0 param) — **Cocok** |
| `print.scm` | Pemanggilan `call` dengan predikat `(#eq? @fn "print")` | 10 pemanggilan ditemukan pada baris 20, 31, 83, 86, 106–110, dan 123 — **Cocok** |
| `import.scm` | `import_statement` dan `import_from_statement` | 6 modul ditemukan (`json`, `math`, `os`, `datetime`, `pathlib`, `typing`) — **Cocok** |
| `docstring.scm` | String baris pertama `block` fungsi (Pengayaan) | 8 docstring fungsi tertangkap (`__init__` tidak memiliki docstring) — **Cocok** |

**Inti Keluaran Terminal (`python q.py uji_100_baris.py <file.scm>`):**
=== 1. Fungsi ===
Pohon S-expression:
(module (function_definition name: (identifier) parameters: (parameters (identifier)) body: (block (return_statement (identifier)))))

Anak langsung dari 'function_definition':
  - 'def' -> anonim
  - 'identifier' -> bernama
  - 'parameters' -> bernama
  - ':' -> anonim
  - 'block' -> bernama
Anak dari 'parameters':
  - '(' -> anonim
  - 'identifier' -> bernama
  - ')' -> anonim

=== 2. If-Else ===
Pohon S-expression:
(module (if_statement condition: (comparison_operator (identifier) (integer)) consequence: (block (expression_statement (assignment left: (identifier) right: (integer)))) alternative: (else_clause body: (block (expression_statement (assignment left: (identifier) right: (integer)))))))

Anak langsung dari 'if_statement':
  - 'if' -> anonim
  - 'comparison_operator' -> bernama
  - ':' -> anonim
  - 'block' -> bernama
  - 'else_clause' -> bernama

=== 3. Kelas ===
Pohon S-expression:
(module (class_definition name: (identifier) body: (block (function_definition name: (identifier) parameters: (parameters (identifier)) body: (block (return_statement (identifier)))))))

Anak langsung dari 'class_definition':
  - 'class' -> anonim
  - 'identifier' -> bernama
  - ':' -> anonim
  - 'block' -> bernama

=== 4. Simulasi Syntax Error ===
(module (ERROR (identifier) (parameters (identifier)) (identifier)))

## 2. Ringkasan Pelaksanaan & Hasil Tugas 4–6 (`tree-sitter-filter/` & `cek/`)

### Tugas 4 — Grammar DSL Filter Admin (`grammar.js` & `test/corpus/dasar.txt`)
Grammar `filter` dibangun bertahap untuk mendukung ekspresi pencarian admin enterprise, mencakup perbandingan (`=`, `!=`, `>`, `<`, `>=`, `<=`), operator logika dengan tingkat presedensi `prec.left(1)` untuk `or`, `prec.left(2)` untuk `and`, `prec(3)` untuk `not`, pengelompokan tanda kurung, serta operator `in_expression` dan `contains_expression`. Enam kasus uji ditulis pada `test/corpus/dasar.txt` dan seluruhnya lulus perintah `tree-sitter test`.

**Inti Keluaran Terminal (`tree-sitter test`):**
PS C:\PLP 2B_JTK\PLP PR MINGGU 10\tugas1-3> cd "C:\PLP 2B_JTK\PLP PR MINGGU 10\tree-sitter-filter"
>> tree-sitter generate
>> tree-sitter test
  dasar:
      1. ✓ 1. and lebih kuat dari or
      2. ✓ 2. tanda kurung mengubah prioritas
      3. ✓ 3. operator not dan nilai boolean
      4. ✓ 4. perbandingan string dan field bertitik
      5. ✓ 5. operator in dengan tiga nilai
      6. ✓ 6. operator contains untuk pencarian teks

Total parses: 6; successful parses: 6; failed parses: 0; success percentage: 100.00%; average speed: 1180 bytes/ms

PS C:\PLP 2B_JTK\PLP PR MINGGU 10\tree-sitter-filter> 

### Tugas 5 — Syntax Highlighting DSL Filter (`queries/highlights.scm`)
Aturan pewarnaan memetakan kata kunci (`and`, `or`, `not`, `in`, `contains`) ke `@keyword`, operator ke `@operator`, literal ke `@string`/`@number`/`@constant.builtin`, serta nama kolom pada setiap ekspresi ke `@property`. Pengujian pada `contoh.filter` menggunakan `tree-sitter highlight contoh.filter` menampilkan pewarnaan berbeda untuk setiap kategori token.

S C:\PLP 2B_JTK\PLP PR MINGGU 10\tree-sitter-filter> cd "C:\PLP 2B_JTK\PLP PR MINGGU 10\tree-sitter-filter"
>> tree-sitter highlight contoh.filter
Warning: You should add a `highlights` entry pointing to the highlights.scm path in the `tree-sitter` object in the grammar's tree-sitter.json file. See more here: https://tree-sitter.github.io/tree-sitter/3-syntax-highlighting#query-paths
not archived = true and (status in ("open", "pending") or priority >= 2) and title contains "invoice"
PS C:\PLP 2B_JTK\PLP PR MINGGU 10\tree-sitter-filter> 

### Tugas 6 — Mini Proyek CLI Pendeteksi Kualitas Kode (`cek/cek.py`)
Skrip `cek.py` memindai berkas `*.py` secara rekursif sambil mengabaikan direktori `.git`, `venv`, dan `__pycache__`. Program mendeteksi komentar `TODO`/`FIXME` via query `#match?`, fungsi berdurasi lebih dari 30 baris melalui selisih `end_point[0] - start_point[0] + 1`, serta berkas bermasalah lewat `root_node.has_error` dan pencarian rekursif node `ERROR`/`MISSING` pertama. Pengujian berhasil pada folder buatan `uji/` maupun repositori open-source `pallets/click` dengan verifikasi manual pada 2 berkas acak.

>> python cek.py uji                  
[SYNTAX ERROR] uji\contoh_error.py:1:3: ditemukan 'ERROR'
[FUNGSI PANJANG] uji\contoh_panjang.py:1: 'proses_panjang' (36 baris)
[TODO/FIXME] uji\contoh_todo.py:2: # TODO: tambahkan validasi input negatif
[TODO/FIXME] uji\contoh_todo.py:4: # FIXME: tangani kasus overflow
[FUNGSI PANJANG] repo_uji\examples\termui\termui.py:38: 'progress' (63 baris)
[FUNGSI PANJANG] repo_uji\src\click\__init__.py:76: '__getattr__' (69 baris)
[FUNGSI PANJANG] repo_uji\src\click\_compat.py:241: '_force_correct_text_stream' (44 baris)
[FUNGSI PANJANG] repo_uji\src\click\_compat.py:374: 'open_stream' (79 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:44: '__init__' (70 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:250: 'render_progress' (45 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:349: 'generator' (32 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:449: '_pager_contextmanager' (43 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:547: '_pipepager' (84 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:634: '_tempfilepager' (32 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:749: 'edit' (46 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:797: 'open_url' (68 baris)
[FUNGSI PANJANG] repo_uji\src\click\_termui_impl.py:885: 'getchar' (45 baris)
[FUNGSI PANJANG] repo_uji\src\click\_textwrap.py:20: '_wrap_chunks' (57 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:368: '__init__' (174 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:596: 'scope' (36 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:884: 'invoke' (51 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1059: '__init__' (43 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1126: 'get_params' (55 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1216: 'get_help_option' (33 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1353: 'make_context' (36 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1390: 'parse_args' (32 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1439: 'shell_complete' (46 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1506: 'main' (135 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1642: '_main_shell_completion' (31 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1753: '__init__' (54 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1844: 'command' (40 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1893: 'group' (43 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:1937: 'result_callback' (44 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2043: 'invoke' (67 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2397: '__init__' (80 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2520: '_check_name_is_usable' (36 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2632: 'get_default' (32 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2668: 'consume_value' (47 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2716: 'type_cast_value' (55 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2790: 'process_value' (61 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2852: 'resolve_envvar_value' (44 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:2913: 'handle_parse_result' (87 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3133: '__init__' (76 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3232: '_infer_flag_kind' (32 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3265: '_pick_type' (38 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3372: 'get_default' (31 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3434: '_parse_decls' (66 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3501: 'add_to_parser' (41 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3599: 'get_help_extra' (82 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3682: 'prompt_for_value' (48 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3755: 'value_from_envvar' (47 baris)
[FUNGSI PANJANG] repo_uji\src\click\core.py:3803: 'consume_value' (55 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:47: 'make_pass_decorator' (47 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:96: 'pass_meta_key' (31 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:164: 'command' (88 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:213: 'decorator' (34 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:417: 'version_option' (136 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:495: 'callback' (48 baris)
[FUNGSI PANJANG] repo_uji\src\click\decorators.py:555: 'custom_version_option' (40 baris)
[FUNGSI PANJANG] repo_uji\src\click\exceptions.py:184: 'format_message' (39 baris)

.... lebih panjang lagi
## 3. Kendala Teknis & Cara Mengatasinya

| Tugas | Kendala yang Ditemui | Solusi & Langkah Perbaikan |
| :--- | :--- | :--- |
| **Tugas 1 & 3** | Redirection terminal PowerShell (`>` dan `\| Out-File`) menghasilkan berkas `.txt` kosong atau hanya berisi judul saat terjadi masalah encoding/stderr. | Menulis keluaran langsung melalui Python (`Path.write_text(..., encoding="utf-8")`) dan `subprocess.run(..., capture_output=True)` agar stdout dan stderr tertangkap utuh. |
| **Tugas 4** | Perintah `tree-sitter generate` gagal dengan pesan `ReferenceError: module is not defined in ES module scope` pada Node.js v24.14.1. | Mengubah deklarasi awal `grammar.js` dari sintaks CommonJS (`module.exports = grammar(...)`) menjadi sintaks ES Module (`export default grammar(...)`). |
| **Tugas 4** | Muncul `Unresolved conflict` saat menambahkan `or_expression` dan `and_expression` secara bersamaan. | Menetapkan asosiasi kiri dan bobot prioritas bertingkat memakai `prec.left(1, ...)` untuk `or` dan `prec.left(2, ...)` untuk `and`. |
| **Tugas 4 & 5** | Folder `test/corpus/` tidak otomatis terbentuk saat `tree-sitter init`, dan `tree-sitter highlight` belum mengenali berkas `.filter`. | Membuat direktori `test\corpus\` secara manual serta mendaftarkan folder induk proyek ke array `"parser-directories"` di `config.json`. |

---

## 4. Catatan Penggunaan AI Coding Agent & Bukti Verifikasi

Selama pengerjaan Tugas 1–6, AI coding agent digunakan sebagai asisten pemandu sintaks API `py-tree-sitter` versi terbaru, struktur query S-expression, serta penyusunan kasus uji. Berikut rincian permintaan, temuan kesalahan hasil AI, dan bukti verifikasinya:

| Bagian | Permintaan ke AI | Kesalahan / Kekurangan Hasil AI | Bukti Verifikasi |
| :--- | :--- | :--- | :--- |
| **Tugas 1–3** | Membuat skrip penyimpanan output otomatis dan contoh kode Python $\ge 100$ baris untuk pengujian traversal serta query. | Saran awal memakai operator redirection terminal PowerShell (`>` dan `\| Out-File`) menyebabkan berkas `hasil_t3.txt` kosong tanpa isi hasil query. | Pemeriksaan isi berkas menunjukkan hanya header yang tertulis; setelah diganti penulisan file langsung dari Python, seluruh 9 fungsi, 10 `print`, dan 6 `import` tercetak dan cocok dengan hitungan manual. |
| **Tugas 4–5** | Menyusun kerangka `grammar.js` DSL filter beserta konfigurasi `tree-sitter highlight` di Windows. | Kode awal AI memakai `module.exports = grammar(...)`, padahal `tree-sitter init` terbaru menghasilkan `package.json` dengan `"type": "module"` sehingga gagal dijalankan. | Terminal menampilkan `ReferenceError: module is not defined in ES module scope`. Setelah diubah menjadi `export default grammar(...)`, perintah `tree-sitter generate` sukses dan `tree-sitter test` lulus 6/6 tes. |
| **Tugas 6** | Merancang skrip CLI `cek.py` untuk mendeteksi `TODO`, fungsi panjang, dan *syntax error* pada direktori proyek. | Pada pengujian repo besar, pemindaian awal tanpa pengecualian direktori internal berpotensi memproses folder lingkungan virtual atau cache. | Ditambahkan filter `FOLDER_DIABAIKAN` (`.git`, `venv`, `__pycache__`) dan diuji pada `uji/` serta repo `pallets/click` dengan kecocokan 100% pada 2 berkas yang dicek manual. |