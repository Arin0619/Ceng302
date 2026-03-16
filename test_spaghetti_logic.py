import unittest
import tempfile
from pathlib import Path

from spaghetti_logic import (
    apply_markup,
    format_total,
    log_results,
    process_data,
)


class TestSpaghettiLogic(unittest.TestCase):
    def test_apply_markup(self):
        self.assertAlmostEqual(apply_markup(100, 0.15), 115.0)
        self.assertAlmostEqual(apply_markup(0, 0.5), 0.0)

    def test_format_total(self):
        self.assertEqual(format_total(12.3456), "Total: 12.35")
        self.assertEqual(format_total(5, prefix="Sum:"), "Sum: 5.00")

    def test_process_data_normal(self):
        data = [10, 20]
        out = process_data(data, rate=0.1, log_file=tempfile.gettempdir() + "\\test_log.txt", verbose=False)
        self.assertEqual(len(out), 2)
        self.assertAlmostEqual(out[0], 11.0)
        self.assertAlmostEqual(out[1], 22.0)

    def test_process_data_empty(self):
        out = process_data([], verbose=False)
        self.assertEqual(out, [])

    def test_process_data_invalid_iterable(self):
        with self.assertRaises(TypeError):
            process_data(123, verbose=False)  # not iterable

    def test_process_data_invalid_item(self):
        with self.assertRaises(TypeError):
            process_data(["a", "b"], verbose=False)

    def test_log_results_writes_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
        try:
            # write
            log_results([1, 2, 3], filename=tmp_name)
            contents = Path(tmp_name).read_text(encoding="utf-8")
            self.assertIn("[1, 2, 3]", contents)
        finally:
            Path(tmp_name).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
