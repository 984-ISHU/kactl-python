#!/usr/bin/env python3
"""Fix Python docstrings to work with KACTL preprocessor"""

import os
import re
import sys

def fix_docstring(content):
    """Add * prefix to docstring lines for preprocessor compatibility"""
    # Find docstring (""" at start)
    pattern = r'^"""(.*?)"""'
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    
    if not match:
        return content
    
    docstring = match.group(1)
    lines = docstring.split('\n')
    
    # Add * to non-empty lines
    fixed_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Add * prefix if not already there
            if not stripped.startswith('*'):
                fixed_lines.append(' * ' + stripped)
            else:
                fixed_lines.append(' ' + stripped)
        else:
            fixed_lines.append(line)
    
    fixed_docstring = '\n'.join(fixed_lines)
    new_content = content[:match.start()] + '"""' + fixed_docstring + '"""' + content[match.end():]
    
    return new_content

def process_file(filepath):
    """Process a single Python file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = fix_docstring(content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {filepath}")
        return True
    return False

def main():
    """Process all Python files in content directory"""
    count = 0
    for root, dirs, files in os.walk('content'):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    count += 1
    print(f"\nTotal files fixed: {count}")

if __name__ == '__main__':
    main()
