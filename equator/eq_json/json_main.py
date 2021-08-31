"""json_main.py

Contains main function for json IO
"""
    
import json

from equator import equate, EqExternalException

def json_main():
    try:
        while True:
            try:
                print(json.dumps(equate(input()), indent=None))
            except EqExternalException as e:
                print(str(e))
    except EOFError:
        return
