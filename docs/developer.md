
# Developer

The following are instructions for developers.

## The obvious...

Why oh why did you pick windows!?!? - Well... the author wanted to target windows first because, in truth,
most people using this tool are likely to be gaming on a windows machine.  The author has tons of linux
experience and recognizes that Linux/Dockerized platforms are entirely relevant and in the future.

## Pre-requisites

This software was developed on Windows 10. The chosen software language is Python 3, which can be installed
on any flavor of Linux or Windows.  However, a python environment is a hard requirement. The author used VSCode to
develop software, although any IDE may be used which is the preference of the developer.

1. Python 3 - (See section about python setup.)
2. VSCode + Python Extension (or other preferred IDE)
3. Steam - On Windows, you must have steam installed!
4. Git

Finally - I'm assuming the reader has some software development experience.  Please don't make an issue because you
don't know how to set something up or use an IDE.  Please do make an issue if these instrutions need updating.  Also,
feel free to figure out what's different and make a change yourself ;).

## Development Workflow

The [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
is used and is enforced.

All features get stacked up in the develop branch and then, after testing, released to the main branch.
GitHub Actions automate DevOps Continuous Integration checks along the way.  On the main branch, however,
a packaged release of Agent Smith is generated and attached to the release section.

## Development Environment Preparation

### Ubuntu/Debian Based Linux

Please note that development on linux is experimental for now.  In the future, it will be supported
but not until a later release.  And when that time comes, Ubuntu/Debian will likely be the first
distro supported.

1. sudo apt update
2. sudo apt install python3 python3-venv python3-pip lib32gcc-s1
3. sudo apt install libgl1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
   libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-dev

NOTE:
   - The final step installs a number of required items for PyQt5 applications.
   - You may develop on Linux but the software hasn't been built to do both Windows and Linux yet, so don't build
     something that only works on Linux.

## Windows

1. Download python from here: https://www.python.org/downloads/ - Python 3.10+ will do.
2. install to windows.
3. Open a powershell and test that one can run the "python" command to verify python is installed.
4. install git for windows from here: https://git-scm.com/download/win

## Docker

The backend flask server could be containerized and the PyQT GUI could just simply communicate with
a container, but this has yet to be developed.

# Development Environment

## Stand Alone & Development

One must create a python virtual environment.  Therefore python3 must be present and configured on your machine.

1. python3 -m venv venv/
2. Activate the Python environment:
   - linux: source venv/bin/activate
   - windows:  .\venv\bin\Activate.ps1
3. pip install -U pip
4. pip install -r requirements.txt
5. pip install -r test-requirements.txt
6. Run the backend server: python .\server.py
7. Run the frontend GUI: python .\gui.py

NOTE:
   - There is another script (python .\agent-smith.py), and that can be used to run both the backend server and the front
     end GUI simultaneously.  Use this for final testing of features.
   - The backend server operates on port 5000, and the frontend GUI is built to use that port by default.
     That port should never change. Nginx is used to expose ports and that's where changes are made to
     port numbers.

**Warning**: If one is using a windows only environment, the second step where the python virtual environment is activated
may require a windows policy to be enabled which allows powershell scripts to be run.  This is a windows security
mechanism.  One need only enable the policy and repeat the step.  [Here is more information](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3)
to set this up properly.

## Testing

This software uses the coverage and pytest python packages for a testing framework.  All tests are in the "tests" folder,
and are split up by unit tests and functional tests.  Any unit test is a simple test of a singular function or independent
object.  A functional test is

# Software Development Process

## Documentation & Code Quality

All that fun stuff is going to be [here](./software-code-quality.md).  Really, have a read, PR's depend on it!

Grumble? I tried to keep it simple...

## Software Testing

1. Before code submission run: coverage run -m pytest  (All tests must pass)
2. Create a Pull Request
3. Wait for GitHub actions to run to completion.

## Debugging

This section will speak toward using VSCode for debugging.  A launch configuration is a named JSON object that VSCode
uses to start up a debug session.  There are two relevant to debugging:

1. "Python: Server" - Run this to get a debug session for the backend Flask Server
2. "Python: GUI" - Run this to get a debug session for the frontend PyQt GUI.

The user may use one or the other, or both at the same time.

NOTES:
   - **DO NOT** use print statements to write variables to the terminal in as opposed to proper debugging and expect
     that to get merged!
   - I'm not going to leave instrutions for which buttons to click on VSCode to use the debugger.

## References:

1. https://coverage.readthedocs.io/en/7.3.0/
2. https://git-scm.com/download/win