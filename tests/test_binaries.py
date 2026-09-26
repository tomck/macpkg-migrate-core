"""Host binary vocabulary and install_method: ranking-only, never confidence."""
import unittest

from macpkg_migrate_core import (
    Candidate,
    binary_rank,
    choose_candidate,
    host_bins,
    install_method,
    plan_record,
)
from macpkg_migrate_core.core import Identity


class HostBinsTests(unittest.TestCase):
    def test_intel_sonoma_tokens(self):
        tokens = host_bins("Darwin", "x86_64", 14)
        self.assertIn("sonoma", tokens)
        self.assertIn("darwin_23.x86_64", tokens)
        self.assertNotIn("arm64_sonoma", tokens)

    def test_arm_sequoia_tokens(self):
        tokens = host_bins("Darwin", "arm64", 15)
        self.assertIn("arm64_sequoia", tokens)
        self.assertIn("darwin_24.arm64", tokens)

    def test_linux_tokens(self):
        self.assertEqual(host_bins("Linux", "x86_64"), {"x86_64_linux"})

    def test_unknown_platform_is_empty(self):
        self.assertEqual(host_bins("Darwin", "ppc", 9), set())


class InstallMethodTests(unittest.TestCase):
    def test_empty_is_unknown_never_source(self):
        self.assertEqual(install_method([], {"sonoma"}), "unknown")

    def test_any_is_binary(self):
        self.assertEqual(install_method(["any"], set()), "binary")

    def test_match_is_binary(self):
        self.assertEqual(install_method(["sonoma"], {"sonoma", "darwin_23.x86_64"}), "binary")

    def test_mismatch_is_source(self):
        self.assertEqual(install_method(["darwin_24.arm64"], {"sonoma"}), "source")


class BinaryRankTests(unittest.TestCase):
    def test_binary_beats_unknown_beats_source(self):
        host = {"sonoma"}
        self.assertEqual(binary_rank(["sonoma"], host), 0)
        self.assertEqual(binary_rank([], host), 1)
        self.assertEqual(binary_rank(["darwin_24.arm64"], host), 2)

    def test_accepts_candidate_and_mapping(self):
        host = {"sonoma"}
        candidate = Candidate.from_relation({
            "target": {"manager": "macports", "package_type": "port",
                       "native_name": "wget", "binaries": ["sonoma"]},
            "confidence": 1.0, "review_status": "automatic",
        })
        self.assertEqual(candidate.binaries, ("sonoma",))
        self.assertEqual(binary_rank(candidate, host), 0)
        self.assertEqual(binary_rank({"binaries": ["sonoma"]}, host), 0)
        self.assertEqual(
            binary_rank({"target": {"binaries": ["sonoma"]}}, host), 0)

    def test_fink_bindist_tokens_rank(self):
        tokens = host_bins("Darwin", "x86_64", 9)
        self.assertIn("10.14/binary-darwin-x86_64", tokens)
        self.assertEqual(
            binary_rank(["10.14/binary-darwin-x86_64"], tokens), 0)


class ChooseCandidateBinaryTests(unittest.TestCase):
    def _candidate(self, name, confidence, binaries, status="automatic"):
        return Candidate.from_relation({
            "target": {"manager": "macports", "package_type": "port",
                       "native_name": name, "binaries": binaries},
            "confidence": confidence, "review_status": status,
        })

    def test_prefers_binary_over_higher_confidence_source(self):
        host = {"sonoma"}
        binary = self._candidate("wget-bin", 0.9, ["sonoma"])
        source = self._candidate("wget-src", 1.0, ["darwin_24.arm64"])
        self.assertEqual(choose_candidate([source, binary], host=host), binary)

    def test_safety_still_wins_over_binary(self):
        host = {"sonoma"}
        review_binary = self._candidate("a", 1.0, ["sonoma"], "needs-review")
        auto_source = self._candidate("b", 0.9, ["darwin_24.arm64"])
        self.assertEqual(
            choose_candidate([review_binary, auto_source], host=host), auto_source)

    def test_plan_record_carries_install_method(self):
        host = {"sonoma"}
        candidates = [self._candidate("wget", 1.0, ["sonoma"])]
        record = plan_record(
            Identity("homebrew", "formula", "wget"), candidates, "v1", host=host)
        self.assertEqual(record["recommendation"]["install_method"], "binary")
        self.assertEqual(record["recommendation"]["binaries"], ["sonoma"])


if __name__ == "__main__":
    unittest.main()
