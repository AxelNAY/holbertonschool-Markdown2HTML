#!/usr/bin/python3
"""Write a script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name"""

import os
import re
import sys

def format_text(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        exit(1)

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    with open(sys.argv[2], 'w') as file:
        unorder_status = False
        order_status = False
        text_status = False
        line_prec = None
        for line in lines:
            length = len(line)
            stripped = line.strip()
            headings = line.lstrip('#')
            heading_count = length - len(headings)
            unorder_list = line.lstrip('-')
            unorder_count = length - len(unorder_list)
            order_list = line.lstrip('*')
            order_count = length - len(order_list)
            bold = line.lstrip('**')
            bold_count = length - len(bold)
            italic = line.lstrip('__')
            italic_count = length - len(italic)

            is_text_line = (
                stripped != "" and
                heading_count == 0 and
                unorder_count == 0 and
                order_count == 0
            )

            if 1 <= heading_count <= 6:
                line = '<h{}>'.format(
                    heading_count) + headings.strip(
                    ) + '</h{}>\n'.format(heading_count)

            elif unorder_count:
                if not unorder_status:
                    file.write('<ul>\n')
                    unorder_status = True
                content = format_text(unorder_list.strip())
                line = f'<li>{content}</li>\n'
            elif unorder_status and not unorder_count:
                file.write('</ul>\n')
                unorder_status = False

            elif order_count:
                if not order_status:
                    file.write('<ol>\n')
                    order_status = True
                content = format_text(unorder_list.strip())
                line = f'<li>{content}</li>\n'
            elif order_status and not order_count:
                file.write('</ol>\n')
                order_status = False

            elif is_text_line:
                if not text_status:
                    file.write('<p>\n')
                    text_status = True
                content = format_text(unorder_list.strip())
                line = f'{content}\n'
                if line_prec.strip() != "":
                    file.write('<br/>\n')
                
            elif text_status and stripped == "":
                file.write('</p>\n')
                text_status = False

            if stripped != "":
                file.write(line)
            line_prec = line
        if unorder_status:
            file.write('</ul>\n')
        if order_status:
            file.write('</ol>\n')
        if text_status:
            file.write('</p>\n')

    exit(0)
