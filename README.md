# Equator
A maths interpreter built in Python using SymPy

[![Pytest](https://github.com/MiguelGuthridge/Equator/actions/workflows/python-app.yml/badge.svg)](https://github.com/MiguelGuthridge/Equator/actions/workflows/python-app.yml)

# Features:
* Solve simultaneous equations
* Simplify expressions
* It can do maths faster than you

# Installation

Equator can be installed from PyPi. Run the command
```
pip3 install equatorpy
```

# Usage:

## Start-up:
Equator can be run directly through the Python module. Run the command
```
python3 -m equator
```
Alternatively, Equator can be invoked directly using the command
```
equator
```
The program has been tested on Windows and Linux (Ubuntu), but not MacOS. It might work, but it might not.
* If no arguments are provided, the program launches into a full interpreter, built using the Curses library.
* If it is started with the argument `json`, then its output will be in a JSON format, where each line of input is treated as one set of equations and expressions. Each input will have one line of respective output, in [JSON format](https://github.com/MiguelGuthridge/Equator/wiki/JSON-Format-Specification).
* If it is started with the argument `ev`, then it will run a quick evaluation on the following argument. For example `equator ev "1 + 1"` would print `2`.

## Syntax:
* Order of operations is respected (including brackets)
* Use standard mathematical syntax (+, -, *, /, ^, =, etc)
* Functional notation is used for unary operators:
    * `|A|` should be written as `abs(A)`
* Equations or expressions are separated by semicolons

# Development

When working with Equator, it is recommended to work with a virtual environment.

After `git clone`ing the repository, set up a virtual environment using [these
instructions](https://docs.python.org/3/library/venv.html), then install the
required dependencies using the command
```
pip3 install -r requirements.txt
```
or if you're on Windows
```
pip install -r requirements_windows.txt
```

You should then be able to debug or develop the interpreter normally.
