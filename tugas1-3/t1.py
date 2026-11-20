from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

potongan_kode = {
    "1. Fungsi": b"def sapa(nama):\n    return nama\n",
    "2. If-Else": b"if x > 0:\n    y = 1\nelse:\n    y = 0\n",
    "3. Kelas": b"class Mahasiswa:\n    def info(self):\n        return self\n",
}

baris_output = []

for judul, kode in potongan_kode.items():
    baris_output.append(f"=== {judul} ===")
    tree = parser.parse(kode)
    baris_output.append("Pohon S-expression:")
    baris_output.append(str(tree.root_node))

    node_utama = tree.root_node.children[0]
    baris_output.append(f"\nAnak langsung dari '{node_utama.type}':")
    for c in node_utama.children:
        status = "bernama" if c.is_named else "anonim"
        baris_output.append(f"  - {c.type!r} -> {status}")

    params = node_utama.child_by_field_name("parameters")
    if params:
        baris_output.append("Anak dari 'parameters':")
        for p in params.children:
            status = "bernama" if p.is_named else "anonim"
            baris_output.append(f"  - {p.type!r} -> {status}")
    baris_output.append("")

baris_output.append("=== 4. Simulasi Syntax Error ===")
kode_rusak = b"def sapa(nama)\n    return nama\n"
tree_rusak = parser.parse(kode_rusak)
baris_output.append(str(tree_rusak.root_node))

hasil_teks = "\n".join(baris_output) + "\n"
print(hasil_teks)

# Simpan langsung di folder yang sama dengan t1.py
output_path = Path(__file__).parent / "hasil_t1.txt"
output_path.write_text(hasil_teks, encoding="utf-8")