# Equator
A maths interpreter built in Python using SymPy

[![Pytest](https://github.com/MiguelGuthridge/Equator/actions/workflows/python-app.yml/badge.svg)](https://github.com/MiguelGuthridge/Equator/actions/workflows/python-app.yml)

# Features:
* Solve simultaneous equations
* Simplify expressions
* It can do maths faster than you

# Usage:

## Start-up:
Run the file `equator.py` in the top-level directory. For example, `python3 equator.py`. The program has been tested on Windows and Linux (Ubuntu), but not MacOS. It might work, but it might not.
* If no arguments are provided, the program launches into a full interpreter, built using the Curses library.
* If it is started with the argument `json`, then its output will be in a JSON format, where each line of input is treated as one set of equations and expressions. Each input will have one line of respective output, in [JSON format](https://github.com/MiguelGuthridge/Equator/wiki/JSON-Format-Specification).
* If it is started with the argument `ev`, then it will run a quick evaluation on the following argument. For example `equator ev "1 + 1"` would print `2`.

## Syntax:
* Order of operations is respected (including brackets)
* Use standard mathematical syntax (+, -, *, /, ^, =, etc)
* Functional notation is used for unary operators:
    * `|A|` should be written as `abs(A)`
* Equations or expressions are seperated by semicolons
