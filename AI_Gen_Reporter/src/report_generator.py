# src/report_generator.py
import os
from pathlib import Path

def load_scanner_results(results_dir='scanner_results'):
    """Load all scanner result files"""
    results = {}

    # Get the absolute path relative to the script location
    script_dir = Path(__file__).parent.parent  # Go up to project root
    results_path = script_dir / results_dir

    # If the path doesn't exist, try relative to current working directory
    if not results_path.exists():
        results_path = Path(results_dir)

    for md_file in results_path.glob('*.md'):
        tool_name = md_file.stem
        with open(md_file, 'r') as f:
            results[tool_name] = f.read()

    return results
