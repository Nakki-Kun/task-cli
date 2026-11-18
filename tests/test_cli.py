import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def jalankan(data, *argumen):
    return subprocess.run(
        [sys.executable, str(ROOT / "task.py"), "--file", str(data), *argumen],
        capture_output=True,
        text=True,
    )


class CliTest(unittest.TestCase):
    """Smoke test: memastikan CLI benar-benar bisa dijalankan dari terminal."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.data = Path(self.folder.name) / "data.json"

    def tulis(self, tasks):
        self.data.write_text(json.dumps(tasks), encoding="utf-8")

    def test_ringkasan(self):
        self.tulis([{"judul": "a", "selesai": True}, {"judul": "b", "selesai": False}])
        hasil = jalankan(self.data, "ringkasan")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("1/2 tugas selesai", hasil.stdout)

    def test_cari(self):
        self.tulis([{"judul": "Belajar Python", "selesai": False}])
        hasil = jalankan(self.data, "cari", "python")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertIn("Belajar Python", hasil.stdout)

    def test_bersihkan(self):
        self.tulis([{"judul": "a", "selesai": True}, {"judul": "b", "selesai": False}])
        hasil = jalankan(self.data, "bersihkan")
        self.assertEqual(hasil.returncode, 0, hasil.stderr)
        self.assertNotIn("[x] a", hasil.stdout)
        self.assertIn("[ ] b", hasil.stdout)


if __name__ == "__main__":
    unittest.main()
