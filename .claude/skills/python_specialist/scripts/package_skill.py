#!/usr/bin/env python3
"""
Simple packaging script for the python_specialist skill
"""

import zipfile
import os
from pathlib import Path

def package_skill(skill_dir: str, output_dir: str = "."):
    """Package the skill into a .skill file"""
    skill_path = Path(skill_dir)
    skill_name = skill_path.name

    output_path = Path(output_dir) / f"{skill_name}.skill"

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arc_path)

    print(f"Skill packaged successfully: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python package_skill.py <skill_directory>")
        sys.exit(1)

    skill_dir = sys.argv[1]
    package_skill(skill_dir)