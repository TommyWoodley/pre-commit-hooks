from __future__ import annotations

import argparse
import os
import re
import subprocess
from typing import Sequence

def convert_to_pdf_with_marp(filename: str, css_template: str | None) -> bool:
    """
    Converts the given markdown file to PDF using marp with an optional CSS template.
    """
    output_file = os.path.splitext(filename)[0] + '.pdf'
    command = ['marp', '--pdf', filename, '-o', output_file]
    if css_template:
        command += ['--theme', css_template]
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        print(f'Error converting {filename} to PDF:\n{result.stderr.decode()}')
        return False
    print(f'Successfully converted {filename} to {output_file}')
    return True

def process_markdown_files(filenames: Sequence[str], pattern: str | None, css_template: str | None) -> int:
    """
    Process markdown files using marp to convert them to PDF with an optional regex pattern and CSS template.
    """
    regex = re.compile(pattern) if pattern else None
    return_code = 0

    for filename in filenames:
        if filename.endswith('.md') and (not regex or regex.search(filename)):
            print(f'Converting {filename} to PDF with custom CSS template...')
            if not convert_to_pdf_with_marp(filename, css_template):
                return_code = 1

    return return_code

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to convert')
    parser.add_argument('--pattern', '-p', help='Regex pattern to match files for conversion. Converts all *.md files if not specified.')
    parser.add_argument('--css', help='Custom CSS template path for Marp conversion.')
    args = parser.parse_args(argv)

    return process_markdown_files(args.filenames, args.pattern, args.css)

if __name__ == '__main__':
    raise SystemExit(main())