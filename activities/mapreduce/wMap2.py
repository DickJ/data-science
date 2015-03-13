#!/usr/bin/python
__author__ = 'rich'

import sys

for line in sys.stdin:
    words = line.split()
    for word in words:
        print word + '\t' + str(1)