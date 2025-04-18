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
        list_status = False
        line_prec = None
        for line in lines:
            length = len(line)
            headings = line.lstrip('#')
            heading_count = length - len(headings)
            unorder_list = line.lstrip('-')
            list_count = length - len(unorder_list)

            if 1 <= heading_count <= 6:
                line = '<h{}>'.format(
                    heading_count) + headings.strip(
                    ) + '</h{}>\n'.format(heading_count)

            if list_count:
                if not list_status:
                    file.write('<ul>\n')
                    list_status = True
                line = '<li>' + unorder_list.strip() + '</li>\n'

            file.write(line)
            line_prec = line
        if list_count:
            file.write('</ul>')

    exit(0)
