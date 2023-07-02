# Private Game Server Manager - Agent

This application is agent software for the Private Game Server Manager

# Pre-requisites

This software was developed on Windows 10 using WSL2 & Docker Desktop for Windows.  WSL2 ran an Ubuntu 18.04 
distribution, however, feel free to use any distribution.  The chosen software language is Python 3, which can be installed
on any flavor of linux.  WSL2 is not strictly required, but python & docker desktop for windows are.  

1. WSL2 Setup - https://learn.microsoft.com/en-us/windows/wsl/install
2. Docker Desktop for Windows - https://www.docker.com/products/docker-desktop/
3. Python3 

## Python Setup

### WSL2 with Ubuntu

1. sudo apt update
2. sudo apt install python3 python3-venv python3-pip

# Usage & Setup

## Docker Deployment

This section details how to build and deploy a docker image that contains this software, and or test with it.

### To build

1. docker compose

## Stand Alone & Development

One must create a python virtual environment.  Therefore python3 must be present and configured on your machine.

1. python3 -m venv venv/
2. source venv/bin/activate
3. pip install -U pip
4. pip install -r requirements.txt 
5. ./main.py or python3 main.py

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

For a dispassionate method to keep the software looking spiffy, use the pythong "black" package.  Simply run "black ."
and your code will magically be styled.  

## Software Testing

TBD - Eventually pytest/tox and github actions will be written to handle this.