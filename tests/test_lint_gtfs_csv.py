import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import lint_gtfs_csv


class TestLintGtfsCsvErrorHandling(unittest.TestCase):
    def test_process_feed_dir_returns_error_when_gtfs_kit_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            feed_dir = Path(tmpdir) / "bad-feed"
            feed_dir.mkdir()

            with patch.object(lint_gtfs_csv.gk, "read_feed", side_effect=ValueError("corrupt feed")):
                status = lint_gtfs_csv.process_feed_dir(feed_dir, fix=True)

            self.assertEqual(status, lint_gtfs_csv.FeedStatus.ERROR)

    def test_process_feed_dir_returns_error_on_file_read_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            feed_dir = data_dir / "feed"
            feed_dir.mkdir()
            (feed_dir / "agency.txt").write_bytes(b"\xff\xfe\x00\x00")

            class DummyFeed:
                def clean(self):
                    return self

            with patch.object(lint_gtfs_csv.gk, "read_feed", return_value=DummyFeed()):
                status = lint_gtfs_csv.process_feed_dir(feed_dir, fix=True)

            self.assertEqual(status, lint_gtfs_csv.FeedStatus.ERROR)

    def test_main_fix_exits_nonzero_on_processing_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            data_dir = root_dir / "data"
            (data_dir / "broken-feed").mkdir(parents=True)

            fake_script = root_dir / "scripts" / "lint_gtfs_csv.py"
            fake_script.parent.mkdir()

            stdout = io.StringIO()
            with (
                patch.object(lint_gtfs_csv, "__file__", str(fake_script)),
                patch.object(sys, "argv", ["lint_gtfs_csv.py", "--fix"]),
                patch.object(lint_gtfs_csv, "process_feed_dir", return_value=lint_gtfs_csv.FeedStatus.ERROR),
                contextlib.redirect_stdout(stdout),
            ):
                with self.assertRaises(SystemExit) as ctx:
                    lint_gtfs_csv.main()

            self.assertEqual(ctx.exception.code, 1)
            self.assertNotIn("successfully processed and formatted", stdout.getvalue())

    def test_main_fix_succeeds_when_only_formatting_differences(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            data_dir = root_dir / "data"
            (data_dir / "dirty-feed").mkdir(parents=True)

            fake_script = root_dir / "scripts" / "lint_gtfs_csv.py"
            fake_script.parent.mkdir()

            stdout = io.StringIO()
            with (
                patch.object(lint_gtfs_csv, "__file__", str(fake_script)),
                patch.object(sys, "argv", ["lint_gtfs_csv.py", "--fix"]),
                patch.object(lint_gtfs_csv, "process_feed_dir", return_value=lint_gtfs_csv.FeedStatus.DIRTY),
                contextlib.redirect_stdout(stdout),
            ):
                lint_gtfs_csv.main()

            self.assertIn("successfully processed and formatted", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
