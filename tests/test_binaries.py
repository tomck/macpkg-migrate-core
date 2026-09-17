"""Host binary vocabulary and install_method: ranking-only, never confidence."""
import unittest

from macpkg_migrate_core import host_bins, install_method


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


if __name__ == "__main__":
    unittest.main()
