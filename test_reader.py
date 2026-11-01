import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mplus_reader import read_output

EX = os.path.join(os.path.dirname(__file__), "..", "examples")


class TestReader(unittest.TestCase):
    def test_cfa(self):
        r = read_output(os.path.join(EX, "cfa_omega.out"))
        self.assertEqual(r["n"], 255443)
        self.assertEqual(r["estimator"], "MLR")
        self.assertEqual(r["fit"]["df"], 41)
        self.assertAlmostEqual(r["fit"]["cfi"], 0.981)
        self.assertAlmostEqual(r["fit"]["rmsea_hi"], 0.038)
        self.assertEqual(sorted(r["latent"]), ["FDISC", "FSECLS", "FSTBEH"])
        omega = [x for x in r["unstd"] if x["name"].startswith("OMEGA")]
        self.assertEqual([round(x["est"], 3) for x in omega], [0.860, 0.707, 0.850])

    def test_sem(self):
        r = read_output(os.path.join(EX, "sem_mediation.out"))
        self.assertEqual(r["n"], 1563)
        e = r["effects_std"][0]
        self.assertEqual((e["from"], e["to"]), ("T3DISC", "T3SECLS"))
        self.assertAlmostEqual(e["total_indirect"][0], -0.131)
        self.assertAlmostEqual(e["direct"][0], -0.180)
        self.assertEqual(len(r["rsquare"]["latent"]), 2)
        self.assertTrue(any("trustworthy" in w for w in r["warnings"]))
        paths = [x for x in r["stdyx"] if x["block"].endswith(" ON")]
        self.assertEqual(len(paths), 7)


if __name__ == "__main__":
    unittest.main()
