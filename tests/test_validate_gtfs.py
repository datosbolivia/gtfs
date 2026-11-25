import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

VALIDATE_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_gtfs.sh"


class TestValidateGtfsScript(unittest.TestCase):
    def _setup_workspace(self, tmpdir: str, java_script: str, make_script: str = "#!/usr/bin/env bash\nexit 0\n", create_zip: bool = True):
        root = Path(tmpdir)
        (root / "scripts").mkdir()
        (root / ".cache").mkdir()
        (root / "dist").mkdir()
        (root / "bin").mkdir()

        script_copy = root / "scripts" / "validate_gtfs.sh"
        shutil.copy2(VALIDATE_SCRIPT, script_copy)
        (root / ".cache" / "gtfs-validator.jar").write_text("dummy jar")

        if create_zip:
            (root / "dist" / "sample.zip").write_text("dummy zip")

        for name, content in [("java", java_script), ("make", make_script)]:
            tool = root / "bin" / name
            tool.write_text(content)
            tool.chmod(tool.stat().st_mode | stat.S_IXUSR)

        env = os.environ.copy()
        env["PATH"] = f"{root / 'bin'}:{env.get('PATH', '')}"
        return script_copy, env

    def test_fails_when_no_zip_files_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            script, env = self._setup_workspace(
                tmpdir,
                java_script="#!/usr/bin/env bash\nexit 0\n",
                create_zip=False,
            )
            res = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("No GTFS zip files found", res.stderr)

    def test_fails_when_report_json_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            script, env = self._setup_workspace(
                tmpdir,
                java_script="#!/usr/bin/env bash\nexit 0\n",
            )
            res = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("did not generate", res.stderr)

    def test_fails_when_system_errors_non_empty(self):
        java_script = """#!/usr/bin/env bash
out_dir=""
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "--output_base" ]]; then out_dir="$2"; shift 2; else shift; fi
done
echo '{"notices":[{"code":"io_error"}]}' > "$out_dir/system_errors.json"
echo '{"notices":[]}' > "$out_dir/report.json"
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            script, env = self._setup_workspace(tmpdir, java_script=java_script)
            res = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("System errors found", res.stderr)

    def test_fails_when_report_json_invalid(self):
        java_script = """#!/usr/bin/env bash
out_dir=""
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "--output_base" ]]; then out_dir="$2"; shift 2; else shift; fi
done
echo 'not json' > "$out_dir/report.json"
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            script, env = self._setup_workspace(tmpdir, java_script=java_script)
            res = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("Could not parse", res.stderr)

    def test_fails_when_report_has_errors(self):
        java_script = """#!/usr/bin/env bash
out_dir=""
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "--output_base" ]]; then out_dir="$2"; shift 2; else shift; fi
done
echo '{"notices":[]}' > "$out_dir/system_errors.json"
echo '{"notices":[{"code":"missing_required_field","severity":"ERROR"}]}' > "$out_dir/report.json"
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            script, env = self._setup_workspace(tmpdir, java_script=java_script)
            res = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("1 Error(s), 0 Warning(s)", res.stdout)

    def test_succeeds_with_warnings_only_and_empty_system_errors(self):
        java_script = """#!/usr/bin/env bash
out_dir=""
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "--output_base" ]]; then out_dir="$2"; shift 2; else shift; fi
done
echo '{"notices":[]}' > "$out_dir/system_errors.json"
echo '{"notices":[{"code":"mixed_case","severity":"WARNING"},{"code":"unknown_col","severity":"INFO"}]}' > "$out_dir/report.json"
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            script, env = self._setup_workspace(tmpdir, java_script=java_script)
            res = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0)
            self.assertIn("0 Error(s), 1 Warning(s)", res.stdout)
            self.assertIn("GTFS Validation completed successfully", res.stdout)


if __name__ == "__main__":
    unittest.main()
