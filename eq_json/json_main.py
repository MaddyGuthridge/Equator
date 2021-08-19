"""json_main.py

Contains main function for json IO
"""
    
import json

from lib import equate

def json_main():
    try:
        while True:
            print(json.dumps(equate(input()), indent=None))
    except EOFError:
        return
