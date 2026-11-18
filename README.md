# task-cli

CLI pencatat tugas sederhana dengan penyimpanan JSON. Tanpa dependensi eksternal,
cukup Python 3.10+.

## Fitur

- `tambah` tugas baru
- `list` semua tugas
- `selesai <nomor>` menandai tugas selesai
- `hapus <nomor>` menghapus tugas
- `ringkasan` menghitung tugas selesai dan yang belum
- `cari <kata>` mencari tugas berdasarkan judul
- `bersihkan` menghapus semua tugas yang sudah selesai
- Data disimpan di `~/.task-cli.json` (bisa diubah dengan `--file`)

## Contoh

```bash
python3 task.py tambah "belajar python"
python3 task.py tambah "nulis README"
python3 task.py list
python3 task.py selesai 1
```

Contoh keluaran:

```text
1. [x] belajar python
2. [ ] nulis README
```

## Menjalankan test

```bash
python3 -m unittest discover -s tests -v
```

## Lisensi

MIT
