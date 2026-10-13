import json
import pathlib
import sys
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engine.live import capture,run_suite,compare_runs,validate_run,sha256
class LiveTests(unittest.TestCase):
    def setUp(self):
        self.suite=json.loads((ROOT/"benchmarks/live-suite.json").read_text())
    def record(self,arm,output):
        return {"run_id":arm,"task_id":"t","arm":arm,"source_kind":"manual-import","source_ref":"local-test",
                "created_at":"2026-10-13T00:00:00Z","outputs":[{"case_id":"math-01","text":output,"sha256":sha256(output.encode())}]}
    def test_capture_real_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);(p/"output.txt").write_text("roots 2 and 3",encoding="utf-8")
            obj=capture(p/"run.json",task_id="t",run_id="r",arm="forge",
                        source_ref="local",output_path=p/"output.txt",case_id="math-01")
            self.assertEqual(obj["outputs"][0]["text"],"roots 2 and 3")
    def test_human_review_not_auto_pass(self):
        r=run_suite(self.suite,self.record("forge","roots 2 and 3"))
        self.assertEqual(r["status"],"fail") # Four domains absent
        self.assertEqual(r["cases"][0]["status"],"needs-human-review")
    def test_checksums(self):
        rec=self.record("forge","roots 2 and 3")
        rec["outputs"][0]["text"]="tampered"
        with self.assertRaises(ValueError):validate_run(rec)
    def test_compare_fail_closed(self):
        with self.assertRaises(ValueError):
            compare_runs(self.suite,self.record("forge","2 and 3"),self.record("forge","2 and 3"))
    def test_five_categories(self):
        self.assertEqual({c["category"] for c in self.suite["cases"]},
                        {"mathematics","research","ui-ux","software","artifact"})
    def test_same_task_not_fake_equivalence(self):
        a=self.record("baseline","2 and 3");b=self.record("forge","2 and 3")
        report=compare_runs(self.suite,a,b)
        self.assertEqual(report["release_gate"],"fail")
        self.assertEqual(report["comparability"]["model_match"],True)
if __name__=="__main__":unittest.main()
