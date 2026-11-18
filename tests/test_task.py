import tempfile
import unittest
from pathlib import Path

import task


class TambahTest(unittest.TestCase):
    def test_tambah_tugas(self):
        tasks = task.tambah([], "belajar python")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["judul"], "belajar python")
        self.assertFalse(tasks[0]["selesai"])

    def test_judul_kosong_ditolak(self):
        with self.assertRaises(ValueError):
            task.tambah([], "   ")


class UbahTest(unittest.TestCase):
    def setUp(self):
        self.tasks = [{"judul": "a", "selesai": False}, {"judul": "b", "selesai": False}]

    def test_tandai_selesai(self):
        task.tandai_selesai(self.tasks, 2)
        self.assertTrue(self.tasks[1]["selesai"])
        self.assertFalse(self.tasks[0]["selesai"])

    def test_nomor_di_luar_batas(self):
        with self.assertRaises(IndexError):
            task.tandai_selesai(self.tasks, 5)

    def test_hapus(self):
        task.hapus(self.tasks, 1)
        self.assertEqual([t["judul"] for t in self.tasks], ["b"])


class PenyimpananTest(unittest.TestCase):
    def test_simpan_dan_muat(self):
        tasks = [{"judul": "ngopi", "selesai": True}]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"
            task.simpan(path, tasks)
            self.assertEqual(task.muat(path), tasks)

    def test_file_belum_ada(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(task.muat(Path(folder) / "kosong.json"), [])


class RingkasanTest(unittest.TestCase):
    def test_hitung(self):
        tasks = [
            {"judul": "a", "selesai": True},
            {"judul": "b", "selesai": False},
            {"judul": "c", "selesai": True},
        ]
        self.assertEqual(task.ringkasan(tasks), {"total": 3, "selesai": 2, "belum": 1})

    def test_kosong(self):
        self.assertEqual(task.ringkasan([]), {"total": 0, "selesai": 0, "belum": 0})


class CariTest(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"judul": "Belajar Python", "selesai": False},
            {"judul": "Nulis README", "selesai": True},
            {"judul": "belajar git", "selesai": False},
        ]

    def test_cari_tanpa_beda_huruf(self):
        hasil = task.cari(self.tasks, "BELAJAR")
        self.assertEqual(len(hasil), 2)

    def test_tidak_ketemu(self):
        self.assertEqual(task.cari(self.tasks, "masak"), [])

    def test_kata_kosong(self):
        with self.assertRaises(ValueError):
            task.cari(self.tasks, "  ")


class BersihkanTest(unittest.TestCase):
    def test_buang_yang_selesai(self):
        tasks = [
            {"judul": "a", "selesai": True},
            {"judul": "b", "selesai": False},
            {"judul": "c", "selesai": True},
        ]
        self.assertEqual(task.bersihkan_selesai(tasks), [{"judul": "b", "selesai": False}])

    def test_semua_belum_selesai(self):
        tasks = [{"judul": "a", "selesai": False}]
        self.assertEqual(task.bersihkan_selesai(tasks), tasks)

    def test_daftar_kosong(self):
        self.assertEqual(task.bersihkan_selesai([]), [])


class TampilanTest(unittest.TestCase):
    def test_daftar_kosong(self):
        self.assertIn("Belum ada tugas", task.tampilkan([]))

    def test_tanda_selesai(self):
        teks = task.tampilkan(
            [{"judul": "a", "selesai": True}, {"judul": "b", "selesai": False}]
        )
        self.assertIn("[x] a", teks)
        self.assertIn("[ ] b", teks)


if __name__ == "__main__":
    unittest.main()
