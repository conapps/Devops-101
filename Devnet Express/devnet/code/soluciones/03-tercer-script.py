"""
Script #3
"""

import sys

NUM = int(sys.argv[1])

if NUM < 1:
    print("I'm less than 1!")
elif NUM > 1:
    print("I'm bigger than 1!")
else:
    print("I'm the default statement!")
