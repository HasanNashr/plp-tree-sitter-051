import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

FOLDER_DIABAIKAN = {".git", "venv", ".venv", "__pycache__", "node_modules"}


def cari_error_pertama(node):
    """Menelusuri pohon secara rekursif untuk menemukan node error/missing pertama."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil is not None:
            return hasil
    return None


def cek_file(path: Path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        baris = node.start_point[0] + 1
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO/FIXME] {path}:{baris}: {teks}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        n_fungsi = cap.get("fungsi", [None])[0]
        n_nama = cap.get("nama", [None])[0]
        if n_fungsi and n_nama:
            jumlah_baris = n_fungsi.end_point[0] - n_fungsi.start_point[0] + 1
            if jumlah_baris > 30:
                nama_fungsi = n_nama.text.decode(errors="replace")
                baris_mulai = n_fungsi.start_point[0] + 1
                print(f"[FUNGSI PANJANG] {path}:{baris_mulai}: '{nama_fungsi}' ({jumlah_baris} baris)")

    # Fitur 3: file yang pohonnya mengandung syntax error
    if tree.root_node.has_error:
        node_err = cari_error_pertama(tree.root_node)
        if node_err:
            baris_err = node_err.start_point[0] + 1
            kolom_err = node_err.start_point[1]
            print(f"[SYNTAX ERROR] {path}:{baris_err}:{kolom_err}: ditemukan '{node_err.type}'")
        else:
            print(f"[SYNTAX ERROR] {path}: pohon mengandung error")


def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Folder tidak ditemukan: {target}")
        sys.exit(1)

    for path in sorted(target.rglob("*.py")):
        if any(bagian in FOLDER_DIABAIKAN for bagian in path.parts):
            continue
        cek_file(path)


if __name__ == "__main__":
    main()