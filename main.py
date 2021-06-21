import sys

import parse
import segment

if __name__ == "__main__":
    print("Calculator thingy")
    print("Press Ctrl+C to quit")
    while True:
        try:
            inp = input("calc > ")
            prep = parse.prepString(inp)
            seg = segment.Segment(prep)
            print(seg.evaluate())
        except Exception as e:
            print(e)
            #raise e
