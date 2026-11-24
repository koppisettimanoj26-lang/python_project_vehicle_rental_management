"""Focused Step 6 tests for safe pipe-delimited file storage."""

import csv
import tempfile
import unittest
from unittest.mock import patch
import os
from pathlib import Path

from file_handler import FileHandler


class FileHandlerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name) / "data"
        self.handler = FileHandler(self.data_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_pipe_delimited_records(self):
        records = [[101, "Car", "Toyota", "Innova", 3500.0, True]]
        self.handler.save_data("vehicles.txt", records)
        self.assertEqual(
            self.handler.load_data("vehicles.txt"),
            [["101", "Car", "Toyota", "Innova", "3500.0", "True"]],
        )

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(self.handler.load_data("missing.txt"), [])

    def test_rejects_pipe_and_newline_in_fields(self):
        for unsafe_value in ("Toyota|Honda", "Toyota\nHonda", "Toyota\rHonda"):
            with self.subTest(value=unsafe_value):
                with self.assertRaises(ValueError):
                    self.handler.save_data("vehicles.txt", [[101, unsafe_value]])
        self.assertFalse((self.data_dir / "vehicles.txt").exists())

    def test_validates_all_files_before_replacing_any(self):
        vehicle_path = self.data_dir / "vehicles.txt"
        vehicle_path.write_text("old vehicle data\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.handler.save_many({
                "vehicles.txt": [[101, "Car"]],
                "customers.txt": [[1, "bad|name"]],
            })
        self.assertEqual(vehicle_path.read_text(encoding="utf-8"), "old vehicle data\n")
        self.assertFalse((self.data_dir / "customers.txt").exists())

    def test_failed_commit_restores_already_replaced_file(self):
        vehicle_path = self.data_dir / "vehicles.txt"
        customer_path = self.data_dir / "customers.txt"
        vehicle_path.write_text("old vehicle data\n", encoding="utf-8")
        customer_path.write_text("old customer data\n", encoding="utf-8")

        real_replace = os.replace
        calls = {"count": 0}

        def fail_second_replace(source, destination):
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("simulated replace failure")
            return real_replace(source, destination)

        with patch("file_handler.os.replace", side_effect=fail_second_replace):
            with self.assertRaises(OSError):
                self.handler.save_many({
                    "vehicles.txt": [[101, "Car"]],
                    "customers.txt": [[1, "Manoj"]],
                })

        self.assertEqual(vehicle_path.read_text(encoding="utf-8"), "old vehicle data\n")
        self.assertEqual(customer_path.read_text(encoding="utf-8"), "old customer data\n")

    def test_filename_cannot_escape_data_folder(self):
        with self.assertRaises(ValueError):
            self.handler.load_data("../outside.txt")

    def test_project_relative_default_folder(self):
        default_handler = FileHandler()
        expected = Path(__file__).resolve().parent / "data"
        self.assertEqual(default_handler.data_folder, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
