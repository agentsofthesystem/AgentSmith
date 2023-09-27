# Style Guide

# Introduction

This is a loose guide to how the python code should look at a minimum.  The author of this software recognizes that 
nothing is perfect, so all code should move toward better styling, documentation, typing (etc..) over time.  Not away
from it and get worse.  Therefore, not all code will immediately look this way, but will get better and better over time.

## Documenation

All files, classes and methods should have pydocstyle type comments.

## Typing / Type Hints

The PEP 484 standard for typing shall be followed and strived for; https://peps.python.org/pep-0484/.

This applies to function signatures, class attributes, and where ever it makes sense.

## Formatting

In general, to take away people arguing this vs that for formatting of code, all formatting will be done by the "black"
python package.  It's not perfect but it's consistent which is the goal.

Before each commit simply tyep "black ." and all source code will be re-formatted.  

For more information, check out black's ReadTheDocs here; https://black.readthedocs.io/en/stable/index.html. 
