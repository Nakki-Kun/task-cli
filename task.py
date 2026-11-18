"""CLI pencatat tugas sederhana berbasis JSON.

Data disimpan di file JSON supaya mudah dibaca dan tidak butuh database.
Logika inti dipisah dari antarmuka terminal agar bisa diuji langsung.
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_PATH = Path.home() / ".task-cli.json"


def tambah(tasks, judul):
    """Tambah satu tugas baru di akhir daftar."""
    judul = judul.strip()
    if not judul:
        raise ValueError("judul tugas tidak boleh kosong")
    tasks.append({"judul": judul, "selesai": False})
    return tasks


def tandai_selesai(tasks, nomor):
    """Tandai tugas nomor tertentu (1-based) sebagai selesai."""
    tugas = _ambil(tasks, nomor)
    tugas["selesai"] = True
    return tasks


def hapus(tasks, nomor):
    """Hapus tugas nomor tertentu (1-based) dari daftar."""
    _ambil(tasks, nomor)
    del tasks[nomor - 1]
    return tasks


def _ambil(tasks, nomor):
    if not 1 <= nomor <= len(tasks):
        raise IndexError(f"nomor tugas {nomor} tidak ada")
    return tasks[nomor - 1]


def simpan(path, tasks):
    """Tulis daftar tugas ke file JSON."""
    path = Path(path)
    path.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def muat(path):
    """Baca daftar tugas dari file JSON, kembalikan list kosong bila belum ada."""
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def tampilkan(tasks):
    """Kembalikan representasi teks daftar tugas untuk dicetak."""
    if not tasks:
        return "Belum ada tugas. Tambah pakai: task.py tambah \"judul\""
    baris = []
    for nomor, tugas in enumerate(tasks, start=1):
        tanda = "[x]" if tugas["selesai"] else "[ ]"
        baris.append(f"{nomor}. {tanda} {tugas['judul']}")
    return "\n".join(baris)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Pencatat tugas sederhana.")
    parser.add_argument("--file", default=str(DEFAULT_PATH), help="lokasi file data JSON")
    sub = parser.add_subparsers(dest="perintah", required=True)

    tambah_cmd = sub.add_parser("tambah", help="tambah tugas baru")
    tambah_cmd.add_argument("judul")

    sub.add_parser("list", help="tampilkan semua tugas")
    sub.add_parser("ringkasan", help="hitung tugas selesai dan belum")

    selesai_cmd = sub.add_parser("selesai", help="tandai tugas selesai")
    selesai_cmd.add_argument("nomor", type=int)

    hapus_cmd = sub.add_parser("hapus", help="hapus tugas")
    hapus_cmd.add_argument("nomor", type=int)

    args = parser.parse_args(argv)
    tasks = muat(args.file)

    try:
        if args.perintah == "tambah":
            tambah(tasks, args.judul)
        elif args.perintah == "selesai":
            tandai_selesai(tasks, args.nomor)
        elif args.perintah == "hapus":
            hapus(tasks, args.nomor)
        elif args.perintah == "list":
            print(tampilkan(tasks))
            return 0
        elif args.perintah == "ringkasan":
            info = ringkasan(tasks)
            print(f"{info['selesai']}/{info['total']} tugas selesai ({info['belum']} belum)")
            return 0
    except (ValueError, IndexError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    simpan(args.file, tasks)
    print(tampilkan(tasks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def ringkasan(tasks):
    """Hitung berapa tugas yang sudah selesai dan yang belum."""
    selesai = sum(1 for tugas in tasks if tugas["selesai"])
    return {"total": len(tasks), "selesai": selesai, "belum": len(tasks) - selesai}
