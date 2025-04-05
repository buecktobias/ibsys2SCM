"""

Go through the whole scs directory and put all files into one large file
"""
import os
from pathlib import Path


def summarize():
    with open('summary.md', 'w') as summary_file:
        for root, _, files in os.walk('../scs'):
            for file in files:
                if not file.endswith('.py'):
                    continue
                try:
                    file_path = os.path.join(root, file)
                    summary_file.write(f"\n---\n##{file_path}:")
                    summary_file.write(f"\n{Path(file_path).read_text(encoding="utf-8")}\n---")
                except (UnicodeEncodeError, UnicodeDecodeError) as e:
                    print(f"Skipping {file_path} due to UnicodeDecodeError: {e}")


if __name__ == '__main__':
    summarize()
