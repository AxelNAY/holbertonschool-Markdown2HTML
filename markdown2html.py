#!/usr/bin/python3
"""Write a script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name"""

import os
import sys

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
        line_prec = None
        for line in lines:
            length = len(line)
            headings = line.lstrip('#')
            heading_count = length - len(headings)
            unorder_list = line.lstrip('-')
            unorder_count = length - len(unorder_list)
            order_list = line.lstrip('*')
            order_count = length - len(order_list)

            if 1 <= heading_count <= 6:
                line = '<h{}>'.format(
                    heading_count) + headings.strip(
                    ) + '</h{}>\n'.format(heading_count)

            if unorder_count:
                if not unorder_status:
                    file.write('<ul>\n')
                    unorder_status = True
                line = '<li>' + unorder_list.strip() + '</li>\n'
            if unorder_status and not unorder_count:
                file.write('</ul>\n')
                unorder_status = False

            if order_count:
                if not order_status:
                    file.write('<ol>\n')
                    order_status = True
                line = '<li>' + order_list.strip() + '</li>\n'
            if order_status and not order_count:
                file.write('</ol>\n')
                order_status = False

            file.write(line)
            line_prec = line
        if unorder_count:
            file.write('</ul>\n')
        if order_count:
            file.write('</ol>\n')

    exit(0)
