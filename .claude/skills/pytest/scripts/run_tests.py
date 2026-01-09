#!/usr/bin/env python3
"""
Run pytest with common useful options.

Usage:
    python run_tests.py [path] [options]

Examples:
    python run_tests.py                      # Run all tests
    python run_tests.py tests/               # Run tests in directory
    python run_tests.py tests/test_api.py    # Run specific file
    python run_tests.py -k "test_login"      # Run tests matching pattern
    python run_tests.py --cov=src            # Run with coverage
    python run_tests.py -x                   # Stop on first failure
    python run_tests.py --lf                 # Run last failed tests only
"""

import subprocess
import sys
from pathlib import Path


def main():
    args = sys.argv[1:]

    # Base pytest command with useful defaults
    cmd = [
        "python", "-m", "pytest",
        "-v",              # Verbose output
        "--tb=short",      # Short traceback format
        "-q",              # Quiet (less output noise)
    ]

    # Check if coverage flag is provided
    if "--cov" in " ".join(args) or any(a.startswith("--cov=") for a in args):
        # Add coverage report options
        if "--cov-report" not in " ".join(args):
            cmd.extend(["--cov-report=term-missing"])

    # Add user-provided arguments
    cmd.extend(args)

    # Default to current directory if no path specified
    has_path = any(
        Path(arg).exists() or arg.startswith("tests")
        for arg in args
        if not arg.startswith("-")
    )
    if not has_path and "." not in args:
        cmd.append(".")

    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
