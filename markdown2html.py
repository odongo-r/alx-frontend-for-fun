#!/usr/bin/python3
"""
This module converts Markdown files to HTML.

It supports headings, unordered and ordered lists, paragraphs, bold, emphasis,
and special formatting like MD5 hashing and removal of 'c' characters.

Usage:
    ./markdown2html.py README.md README.html
"""

import sys
import os
import re
import hashlib

def convert_bold_and_emphasis(line):
    """
    Convert Markdown bold (**text**) and emphasis (__text__) to HTML.
    """
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
    return line

def convert_special(line):
    """
    Convert [[text]] to MD5 hash and ((text)) to text with all 'c' removed.
    """
    line = re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
    line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)
    return line

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    in_list = False
    list_type = None
    in_paragraph = False

    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        for line in md_file:
            line = convert_bold_and_emphasis(line)
            line = convert_special(line)
            if line.startswith('- '):
                if not in_list or list_type != 'ul':
                    if in_list:
                        html_file.write(f"</{list_type}>\n")
                    html_file.write("<ul>\n")
                    in_list = True
                    list_type = 'ul'
                content = line.strip('- ').strip()
                html_file.write(f"<li>{content}</li>\n")
            elif line.startswith('* '):
                if not in_list or list_type != 'ol':
                    if in_list:
                        html_file.write(f"</{list_type}>\n")
                    html_file.write("<ol>\n")
                    in_list = True
                    list_type = 'ol'
                content = line.strip('* ').strip()
                html_file.write(f"<li>{content}</li>\n")
            else:
                if in_list:
                    html_file.write(f"</{list_type}>\n")
                    in_list = False
                if line.strip() == '':
                    if in_paragraph:
                        html_file.write("</p>\n")
                        in_paragraph = False
                else:
                    if not in_paragraph:
                        html_file.write("<p>\n")
                        in_paragraph = True
                    html_file.write(line.strip() + "<br/>\n")
        if in_paragraph:
            html_file.write("</p>\n")

if __name__ == "__main__":
    main()
