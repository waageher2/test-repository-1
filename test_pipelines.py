"""Basic tests to validate Azure Pipelines YAML configurations."""

import os
import yaml
import sys


def get_pipeline_files():
    """Return all YAML pipeline files in the repository root."""
    root = os.path.dirname(os.path.abspath(__file__))
    return [
        os.path.join(root, f)
        for f in os.listdir(root)
        if f.endswith(".yml") and "pipeline" in f
    ]


def test_pipeline_files_exist():
    """Verify that pipeline configuration files exist."""
    files = get_pipeline_files()
    assert len(files) > 0, "No pipeline YAML files found"
    print(f"  Found {len(files)} pipeline file(s)")


def test_pipeline_yaml_valid():
    """Verify that all pipeline YAML files are valid YAML."""
    files = get_pipeline_files()
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "r") as f:
            content = yaml.safe_load(f)
        assert content is not None, f"{filename} is empty"
        assert isinstance(content, dict), f"{filename} is not a valid mapping"
        print(f"  {filename}: valid YAML")


def test_pipeline_has_trigger():
    """Verify that all pipeline files define a trigger."""
    files = get_pipeline_files()
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "r") as f:
            content = yaml.safe_load(f)
        assert "trigger" in content, f"{filename} missing 'trigger' key"
        print(f"  {filename}: has trigger")


def run_tests():
    """Run all test functions and report results."""
    tests = [
        test_pipeline_files_exist,
        test_pipeline_yaml_valid,
        test_pipeline_has_trigger,
    ]
    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            print(f"Running {test_fn.__name__}...")
            test_fn()
            print(f"  PASSED")
            passed += 1
        except AssertionError as e:
            print(f"  FAILED: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
