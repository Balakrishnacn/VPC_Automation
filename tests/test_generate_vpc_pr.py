import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "generate_vpc_pr.py"
SPEC = importlib.util.spec_from_file_location("generate_vpc_pr", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GeneratorTests(unittest.TestCase):
    def test_cidr_requires_network_and_supported_prefix(self):
        self.assertEqual(MODULE.validate_cidr("10.42.0.0/16"), "10.42.0.0/16")
        with self.assertRaises(ValueError):
            MODULE.validate_cidr("10.42.0.1/16")
        with self.assertRaises(ValueError):
            MODULE.validate_cidr("10.42.0.0/12")

    def test_model_config_is_constrained(self):
        config = MODULE.validate_model_config({"name": "dev-vpc", "region": "us-east-1"})
        self.assertEqual(config["name"], "dev-vpc")
        with self.assertRaises(ValueError):
            MODULE.validate_model_config({"name": "bad name", "region": "us-east-1"})

    def test_render_uses_module_and_cidr(self):
        with tempfile.TemporaryDirectory() as directory:
            original = MODULE.OUTPUT_DIR
            MODULE.OUTPUT_DIR = Path(directory)
            try:
                MODULE.render("10.42.0.0/16", MODULE.validate_model_config({"name": "dev-vpc"}))
                content = (Path(directory) / "main.tf").read_text()
                self.assertIn("../../modules/vpc", content)
                self.assertIn('cidr                 = "10.42.0.0/16"', content)
            finally:
                MODULE.OUTPUT_DIR = original


if __name__ == "__main__":
    unittest.main()
