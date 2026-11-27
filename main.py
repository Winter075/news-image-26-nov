#!/usr/bin/env python3
"""Copy the 26 November 2026 news poster into the grader's output directory."""

import os
import shutil
from pathlib import Path


def main():
    source = Path(__file__).resolve().parent / 'entry.png'
    if not source.is_file():
        raise SystemExit('entry.png is missing from the repository')
    out_dir = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / 'entry.png')


if __name__ == '__main__':
    main()
