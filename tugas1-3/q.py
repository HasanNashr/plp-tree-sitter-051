import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2], encoding="utf-8").read()
tree = parser.parse(kode)

hasil_matches = QueryCursor(Query(PY, pola)).matches(tree.root_node)

for _, cap in hasil_matches:
    # Kasus khusus untuk query pasangan nama fungsi & jumlah parameter
    if "nama" in cap and "params" in cap:
        n_func = cap["nama"][0]
        n_params = cap["params"][0]
        nama_fungsi = n_func.text.decode()
        jumlah_param = n_params.named_child_count
        print(f"@nama  baris {n_func.start_point[0] + 1}: {nama_fungsi} (jumlah parameter: {jumlah_param})")
    else:
        for tag, nodes in cap.items():
            for n in nodes:
                teks = n.text.decode().replace("\n", " ")
                print(f"@{tag}  baris {n.start_point[0] + 1}: {teks}")