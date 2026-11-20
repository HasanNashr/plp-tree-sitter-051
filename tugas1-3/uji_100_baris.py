import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PengelolaTugas:
    """Kelas untuk mengelola daftar tugas kuliah dan menghitung statistik nilai."""

    def __init__(self, nama_mahasiswa: str, nim: str):
        self.nama_mahasiswa = nama_mahasiswa
        self.nim = nim
        self.daftar_tugas: List[Dict] = []

    def tambah_tugas(self, judul: str, mata_kuliah: str, skor: float, bobot: int = 1) -> None:
        """Menambahkan item tugas baru ke dalam daftar."""
        if skor < 0 or skor > 100:
            print(f"[PERINGATAN] Skor tidak valid untuk {judul}: {skor}")
            return

        item = {
            "judul": judul,
            "mata_kuliah": mata_kuliah,
            "skor": skor,
            "bobot": bobot,
            "waktu_input": datetime.now().isoformat(),
        }
        self.daftar_tugas.append(item)
        print(f"Tugas '{judul}' berhasil ditambahkan.")

    def hitung_rata_rata(self) -> float:
        """Menghitung rata-rata tertimbang dari seluruh tugas."""
        if not self.daftar_tugas:
            return 0.0

        total_skor = 0.0
        total_bobot = 0
        for tugas in self.daftar_tugas:
            total_skor += tugas["skor"] * tugas["bobot"]
            total_bobot += tugas["bobot"]

        if total_bobot == 0:
            return 0.0
        return round(total_skor / total_bobot, 2)

    def konversi_huruf(self, nilai: float) -> str:
        """Mengonversi nilai angka menjadi indeks huruf."""
        if nilai >= 80.0:
            return "A"
        elif nilai >= 73.0:
            return "AB"
        elif nilai >= 65.0:
            return "B"
        elif nilai >= 60.0:
            return "BC"
        elif nilai >= 50.0:
            return "C"
        else:
            return "D"

    def filter_berdasarkan_matkul(self, mata_kuliah: str) -> List[Dict]:
        """Mengambil daftar tugas berdasarkan nama mata kuliah tertentu."""
        hasil = []
        for item in self.daftar_tugas:
            if item["mata_kuliah"].lower() == mata_kuliah.lower():
                hasil.append(item)
        return hasil

    def simpan_ke_json(self, path_file: str) -> bool:
        """Menyimpan seluruh data tugas ke berkas JSON."""
        target = Path(path_file)
        data = {
            "nama": self.nama_mahasiswa,
            "nim": self.nim,
            "rata_rata": self.hitung_rata_rata(),
            "tugas": self.daftar_tugas,
        }
        try:
            target.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"Data tersimpan di: {target.resolve()}")
            return True
        except OSError as err:
            print(f"Gagal menyimpan file: {err}")
            return False


def hitung_standar_deviasi(daftar_nilai: List[float]) -> float:
    """Menghitung standar deviasi populasi dari kumpulan nilai."""
    jumlah = len(daftar_nilai)
    if jumlah == 0:
        return 0.0
    rata = sum(daftar_nilai) / jumlah
    varians = sum((x - rata) ** 2 for x in daftar_nilai) / jumlah
    return round(math.sqrt(varians), 2)


def cetak_ringkasan(pengelola: PengelolaTugas) -> None:
    """Mencetak laporan ringkas ke konsol."""
    rata = pengelola.hitung_rata_rata()
    grade = pengelola.konversi_huruf(rata)
    semua_skor = [t["skor"] for t in pengelola.daftar_tugas]
    std_dev = hitung_standar_deviasi(semua_skor)

    print("=== RINGKASAN AKADEMIK ===")
    print(f"Mahasiswa : {pengelola.nama_mahasiswa} ({pengelola.nim})")
    print(f"Total Item: {len(pengelola.daftar_tugas)}")
    print(f"Rata-rata : {rata} (Grade: {grade})")
    print(f"Std Dev   : {std_dev}")


def jalankan_simulasi() -> None:
    """Fungsi utama untuk menjalankan simulasi pengujian."""
    tracker = PengelolaTugas("Mahasiswa Informatika", "251524000")
    tracker.tambah_tugas("Modul 1 Tree-sitter", "Teknik Kompilasi", 92.0, 2)
    tracker.tambah_tugas("Praktikum VLAN", "Komunikasi Data", 88.5, 1)
    tracker.tambah_tugas("Trigger PostgreSQL", "Basis Data", 85.0, 2)
    tracker.tambah_tugas("Dekomposisi LU", "Aljabar Linear", 78.0, 1)

    cetak_ringkasan(tracker)
    folder_kerja = os.getcwd()
    print(f"Direktori aktif: {folder_kerja}")


if __name__ == "__main__":
    jalankan_simulasi()