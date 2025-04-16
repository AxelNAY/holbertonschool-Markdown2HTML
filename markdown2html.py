#!/usr/bin/python3
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    if os.path.exists(sys.argv[1]) is False:
        sys.stderr.write("Missing " + sys.argv[1] + "\n")
        exit(1)
    exit(0)
