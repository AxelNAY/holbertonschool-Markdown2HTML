#!/usr/bin/python3
"""Write a script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name"""

import os
import re
import sys


def format_text(text):
    """Markdown for bold and italic"""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


def process_markdown(input_file, output_file):
    """Generate markdown html in the new file"""
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        in_unordered_list = False
        in_ordered_list = False
        in_paragraph = False
        previous_line = ""

        for line in lines:
            stripped = line.strip()

            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            unordered_match = re.match(r'^-\s+(.+)$', stripped)
            ordered_match = re.match(r'^\*\s+(.+)$', stripped)

            if heading_match:
                level = len(heading_match.group(1))
                content = format_text(heading_match.group(2))
                file.write(f'<h{level}>{content}</h{level}>\n')

            elif unordered_match:
                if not in_unordered_list:
                    file.write('<ul>\n')
                    in_unordered_list = True
                content = format_text(unordered_match.group(1))
                file.write(f'<li>{content}</li>\n')

            elif ordered_match:
                if not in_ordered_list:
                    file.write('<ol>\n')
                    in_ordered_list = True
                content = format_text(ordered_match.group(1))
                file.write(f'<li>{content}</li>\n')

            elif stripped == "":
                if in_unordered_list:
                    file.write('</ul>\n')
                    in_unordered_list = False
                if in_ordered_list:
                    file.write('</ol>\n')
                    in_ordered_list = False
                if in_paragraph:
                    file.write('</p>\n')
                    in_paragraph = False

            else:
                content = format_text(stripped)

                if not in_paragraph:
                    file.write('<p>\n')
                    in_paragraph = True

                elif previous_line and previous_line.strip() != "":
                    file.write('<br/>\n')

                file.write(f'{content}\n')

            previous_line = line

        if in_unordered_list:
            file.write('</ul>\n')
        if in_ordered_list:
            file.write('</ol>\n')
        if in_paragraph:
            file.write('</p>\n')


def main():
    """Main function"""
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        return 1

    process_markdown(input_file, output_file)
    return 0


if __name__ == "__main__":
    exit(main())
