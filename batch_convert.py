#!/usr/bin/env python3
"""
Batch conversion helper for KACTL C++ to Python
Generates Python file templates from C++ headers
"""

import os
import re
import sys
from pathlib import Path

def extract_docstring(cpp_file):
    """Extract the /** ... */ comment block"""
    with open(cpp_file, 'r') as f:
        content = f.read()
    
    match = re.search(r'/\*\*(.*?)\*/', content, re.DOTALL)
    if not match:
        return '"""\nNo description available\n"""'
    
    comment = match.group(1)
    lines = []
    for line in comment.split('\n'):
        line = line.strip()
        if line.startswith('*'):
            line = line[1:].strip()
        # Handle special LaTeX commands
        line = line.replace('\\texttt{', '')
        line = line.replace('}', '')
        line = line.replace('$', '')
        if line:
            lines.append(line)
    
    return '"""\n' + '\n '.join(lines) + '\n"""'

def generate_template(cpp_file, py_file):
    """Generate a Python template from C++ file"""
    docstring = extract_docstring(cpp_file)
    
    template = f'''{docstring}

# TODO: Convert C++ implementation to Python
# Original file: {os.path.basename(cpp_file)}

# Add your Python implementation here
pass
'''
    
    with open(py_file, 'w') as f:
        f.write(template)
    print(f"Created template: {py_file}")

def batch_convert_directory(content_dir, chapter):
    """Generate templates for all .h files in a chapter"""
    chapter_dir = os.path.join(content_dir, chapter)
    if not os.path.exists(chapter_dir):
        print(f"Directory not found: {chapter_dir}")
        return
    
    for file in os.listdir(chapter_dir):
        if file.endswith('.h'):
            cpp_file = os.path.join(chapter_dir, file)
            py_file = os.path.join(chapter_dir, file.replace('.h', '.py'))
            
            if os.path.exists(py_file):
                print(f"Skipping (exists): {py_file}")
            else:
                generate_template(cpp_file, py_file)

def update_chapter_tex(content_dir, chapter):
    """Update chapter.tex to use .py instead of .h"""
    chapter_tex = os.path.join(content_dir, chapter, 'chapter.tex')
    if not os.path.exists(chapter_tex):
        print(f"chapter.tex not found in {chapter}")
        return
    
    with open(chapter_tex, 'r') as f:
        content = f.read()
    
    # Replace .h with .py in \\kactlimport statements
    updated = re.sub(r'\\kactlimport\{([^}]+)\.h\}', r'\\kactlimport{\1.py}', content)
    
    if updated != content:
        with open(chapter_tex, 'w') as f:
            f.write(updated)
        print(f"Updated: {chapter_tex}")
    else:
        print(f"No changes needed: {chapter_tex}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python batch_convert.py <content_dir> <chapter>  # Generate templates for chapter")
        print("  python batch_convert.py <content_dir> --all      # Generate templates for all chapters")
        print("  python batch_convert.py <content_dir> --update-tex <chapter>  # Update chapter.tex")
        sys.exit(1)
    
    content_dir = sys.argv[1]
    
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--all':
            chapters = ['graph', 'geometry', 'numerical', 'strings', 'various', 
                       'number-theory', 'math']
            for chapter in chapters:
                print(f"\n=== Processing {chapter} ===")
                batch_convert_directory(content_dir, chapter)
        elif sys.argv[2] == '--update-tex' and len(sys.argv) >= 4:
            update_chapter_tex(content_dir, sys.argv[3])
        else:
            batch_convert_directory(content_dir, sys.argv[2])
