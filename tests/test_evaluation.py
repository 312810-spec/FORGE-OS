import json
import pathlib
import sys
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engine.evaluate import evaluate,compare
from engine.selector import select

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.suite=json.loads((ROOT/"benchmarks/suite.json").read_text())
        self.baseline=json.loads((ROOT/"benchmarks/fixtures/baseline.json").read_text())
        self.candidate=json.loads((ROOT/"benchmarks/fixtures/candidate.json").read_text())
    def test_fixture_regression(self):
        report=compare(self.suite,self.baseline,self.candidate)
        self.assertEqual(report["release_gate"],"pass")
        self.assertEqual(report["improvements"],["route-audit"])
        self.assertEqual(report["regressions"],[])
    def test_missing_case_fails_closed(self):
        self.assertEqual(evaluate(self.suite,{"results":[]})["status"],"fail")
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.suite,{"results":[self.candidate["results"][0]]*2})
    def test_unknown_assertion_rejected(self):
        with self.assertRaises(ValueError):
            evaluate({"cases":[{"id":"x","assertions":[{"type":"made-up"}]}]},
                     {"results":[{"id":"x"}]})
    def test_evidence_cannot_be_empty(self):
        c=json.loads(json.dumps(self.candidate))
        for r in c["results"]:
            if r["id"]=="source-citation":r["evidence"]=[]
        self.assertEqual(evaluate(self.suite,c)["status"],"fail")
    def test_selector_no_model_invocation(self):
        result=select({"capabilities":["deterministic-validation"]})
        self.assertEqual(result["candidate"],"local-python")
        self.assertFalse(result["executed"])
    def test_selector_no_fake_model(self):
        self.assertEqual(select({"capabilities":["generation"]})["status"],"unavailable")
    def test_selector_budget_validation(self):
        with self.assertRaises(ValueError):
            select({"max_cost_per_million_output_tokens":-1})

if __name__=="__main__":unittest.main()
