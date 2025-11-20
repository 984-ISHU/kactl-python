#!/usr/bin/env python3
"""
Helper script to batch convert C++ KACTL files to Python
This provides templates and patterns for manual conversion
"""

import os
import re
import sys

def convert_comment_block(cpp_content):
    """Convert C++ comment block to Python docstring"""
    # Extract /** ... */ comment
    match = re.search(r'/\*\*(.*?)\*/', cpp_content, re.DOTALL)
    if not match:
        return '"""\nNo description available\n"""'
    
    comment = match.group(1)
    # Remove leading * from each line
    lines = []
    for line in comment.split('\n'):
        line = line.strip()
        if line.startswith('*'):
            line = line[1:].strip()
        if line:
            lines.append(line)
    
    return '"""\n' + '\n'.join(lines) + '\n"""'

def list_h_files(directory):
    """List all .h files in a directory"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.h'):
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                print(rel_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        list_h_files(sys.argv[1])
    else:
        print("Usage: python conversion_helper.py <content_directory>")
