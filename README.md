# Private Game Server Manager - Agent

## About

This application is agent software for the Private Game Server Manager.  The agent runs on a standalone windows-based
server and interacts with both 1) the software application it is controlling and 2) may be tied to a manager via an
access key/token method.  If tied to manager software, then the user has full user interface and web control over the
agent.  Otherwise, this agent can stand alone and be operated via a client.  See the "./client" and "./scripts" folder
for examples of client-only usage.   

## Pre-requisites

This software was developed on Windows 10 using WSL2 & Docker Desktop for Windows.  WSL2 ran an Ubuntu 18.04 
distribution, however, feel free to use any distribution.  The chosen software language is Python 3, which can be installed
on any flavor of linux.  WSL2 is not strictly required because one can install python in either a linux or windows
environment.  Docker is also optional because the application can run on its own or inside of a docker container.  
However, a python environment is a hard requirement. The author used VSCode to develop software, although any IDE may be
used which is the preference of the developer.

1. WSL2 Setup - https://learn.microsoft.com/en-us/windows/wsl/install
2. Docker Desktop for Windows - https://www.docker.com/products/docker-desktop/  (Optional)
3. Python 3 - (See section about python setup.)
4. VSCode + Python Extension (or other preferred IDE)

## Python Setup

### WSL2 with Ubuntu

1. sudo apt update
2. sudo apt install python3 python3-venv python3-pip

## Windows without WSL2

1. Download python from here: https://www.python.org/downloads/ - Python 3.10+ will do.
2. install to windows.
3. Open a powershell and test that one can run the "python" command.

# Usage & Setup

## Docker Deployment

This section details how to build and deploy a docker image that contains this software, and or test with it.

### To build

1. docker compose build
2. docker compose up

## Stand Alone & Development

One must create a python virtual environment.  Therefore python3 must be present and configured on your machine.

1. python3 -m venv venv/
2. Activate the Python environment:
   - linux: source venv/bin/activate
   - windows:  .\venv\bin\Activate.ps1
3. pip install -U pip
4. pip install -r requirements.txt 
5. ./main.py or python3 main.py
6. cd scripts
7. python (your-script.py)

**Warning**: If one is using a windows only environment, the second step where the python virtual environment is activated 
may require a windows policy to be enabled which allows powershell scripts to be run.  This is a windows security 
mechanism.  One need only enable the policy and repeat the step.  [Here is more information](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3) to set this up properly.

## Testing

There is a client and a scripts folder.

# Secrets File

Create a file called ".env" and inside of it the following secrets must be added.

1. SECRET_KEY - This is the application secret.
2. COMPOSE_PROJECT_NAME - This is the name of the app for docker compose to use.  Helps with testing. 

# Software Development Process 

## Documentation

This readme will contain most pertinent information or links to other markdown files.  The code itself ought to conform
to pydocs and use pydocstyle to maintain that standard. 

## Software Code Quality

For a dispassionate method to keep the software looking spiffy, use the python "black" package.  Simply run "black ."
and your code will magically be styled.  

## Software Testing

TODO - TBD - Eventually pytest/tox and github actions will be written to handle this.