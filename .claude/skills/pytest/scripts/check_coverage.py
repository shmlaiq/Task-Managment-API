#!/usr/bin/env python3
"""
Check test coverage and enforce thresholds.

Usage:
    python check_coverage.py [source_dir] [--threshold N]

Examples:
    python check_coverage.py                      # Check src/ with 80% threshold
    python check_coverage.py app --threshold 90  # Check app/ with 90% threshold
    python check_coverage.py src --html          # Generate HTML report
"""

import subprocess
import sys
import json
from pathlib import Path


def main():
    args = sys.argv[1:]

    # Parse arguments
    source_dir = "src"
    threshold = 80
    html_report = False

    i = 0
    while i < len(args):
        if args[i] == "--threshold":
            threshold = int(args[i + 1])
            i += 2
        elif args[i] == "--html":
            html_report = True
            i += 1
        elif not args[i].startswith("-"):
            source_dir = args[i]
            i += 1
        else:
            i += 1

    # Check if source directory exists
    if not Path(source_dir).exists():
        # Try common alternatives
        for alt in ["src", "app", "."]:
            if Path(alt).exists():
                source_dir = alt
                break

    print(f"Checking coverage for: {source_dir}")
    print(f"Threshold: {threshold}%")
    print("-" * 50)

    # Build pytest command
    cmd = [
        "python", "-m", "pytest",
        f"--cov={source_dir}",
        "--cov-report=term-missing",
        "--cov-report=json",
        "-q",
    ]

    if html_report:
        cmd.append("--cov-report=html")

    # Run pytest with coverage
    result = subprocess.run(cmd, capture_output=False)

    # Parse coverage results
    coverage_file = Path("coverage.json")
    if coverage_file.exists():
        with open(coverage_file) as f:
            data = json.load(f)

        total_coverage = data.get("totals", {}).get("percent_covered", 0)
        print("\n" + "=" * 50)
        print(f"Total Coverage: {total_coverage:.1f}%")
        print(f"Threshold:      {threshold}%")
        print("=" * 50)

        # Show files below threshold
        files_data = data.get("files", {})
        below_threshold = []
        for filepath, stats in files_data.items():
            file_coverage = stats.get("summary", {}).get("percent_covered", 0)
            if file_coverage < threshold:
                below_threshold.append((filepath, file_coverage))

        if below_threshold:
            print(f"\nFiles below {threshold}% coverage:")
            for filepath, coverage in sorted(below_threshold, key=lambda x: x[1]):
                print(f"  {coverage:5.1f}%  {filepath}")

        # Check threshold
        if total_coverage < threshold:
            print(f"\nFAILED: Coverage {total_coverage:.1f}% is below threshold {threshold}%")
            sys.exit(1)
        else:
            print(f"\nPASSED: Coverage {total_coverage:.1f}% meets threshold {threshold}%")

        # Cleanup
        coverage_file.unlink()

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
