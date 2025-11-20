#!/usr/bin/env python3
"""Fix LaTeX special characters in Python docstrings"""

import os
import re

def escape_latex_in_docstring(content):
    """Escape LaTeX special characters in docstrings"""
    # Find the docstring
    pattern = r'^("""\s*\n)(.*?)(""")' 
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    
    if not match:
        return content, False
    
    docstring = match.group(2)
    original = docstring
    
    # Don't escape if already escaped
    # Escape # but not in already escaped sequences like \#
    docstring = re.sub(r'(?<!\\)#', r'\#', docstring)
    # Escape _ but not in already escaped sequences or LaTeX commands
    docstring = re.sub(r'(?<!\\)_(?![a-zA-Z{}])', r'\_', docstring)
    # Escape ^ but not in already escaped sequences like \^{} or in LaTeX commands like ^{}
    docstring = re.sub(r'(?<!\\)\^(?!{})', r'\^{}', docstring)
    
    if docstring != original:
        new_content = content[:match.start(2)] + docstring + content[match.end(2):]
        return new_content, True
    
    return content, False

def process_file(filepath):
    """Process a single Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changed = escape_latex_in_docstring(content)
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed: {filepath}")
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
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
