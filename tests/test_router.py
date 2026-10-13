import json
import pathlib
import sys
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engine.router import route, load_registry
from engine.checkpoint import write_checkpoint,read_checkpoint

class RoutingTests(unittest.TestCase):
    def test_all_registered_triggers(self):
        registry,_=load_registry()
        for module in registry["modules"]:
            for prefix in module["triggers"]:
                with self.subTest(prefix=prefix):
                    answer=route(prefix+" review workflow")
                    self.assertEqual(answer["status"],"routed")
                    self.assertEqual(answer["modules"][-1]["id"],module["id"])
    def test_longest_prefix(self):
        self.assertEqual(route("UI + UX reverse: landing screen")["modules"][-1]["id"],
                         "reverse-engineering")
    def test_prefix_only(self):
        self.assertEqual(route("RE:")["status"],"routed")
    def test_no_false_positive(self):
        self.assertEqual(route("RE:search isn't a callout")["status"],"unmatched")
        self.assertEqual(route("Please use UI: on this")["status"],"unmatched")
    def test_mutation_is_not_inferred_from_audit(self):
        answer=route("FORGE Assurance: audit the draft")
        self.assertEqual(answer["intent"],"read-only")
        self.assertFalse(answer["requires_approval"])
    def test_high_impact_flag(self):
        answer=route("FORGE Execute: deploy to production")
        self.assertTrue(answer["requires_approval"])
    def test_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/"state.json"
            write_checkpoint(p,"sample","task-1","blocked",{"reason":"no browser"})
            self.assertEqual(read_checkpoint(p)["data"]["reason"],"no browser")
            with self.assertRaises(ValueError):
                write_checkpoint(p,"sample","task-1","magical")
    def test_registry_integrity(self):
        registry,triggers=load_registry()
        self.assertGreaterEqual(len(registry["modules"]),7)
        self.assertEqual(len(triggers),sum(len(m["triggers"]) for m in registry["modules"]))

if __name__=="__main__":
    unittest.main()
