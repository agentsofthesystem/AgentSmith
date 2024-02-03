# Agent Smith

## About

Agent Smith is a self-contained System Tray Application software with Flask Server backend housing
an API, written in Python.  The GUI built with PyQT and uses the [Operator](https://github.com/agentsofthesystem/operator)
client to communicate with the server.

### Features

Some of Agent Smith's core features are:

1. Installation of Supported Game Servers.
2. Ability to Start/Stop/Restarted Game Servers.
3. Provide API Access to external users via API.
4. Security with NGINX/SSL/HTTPS & Token-Based Access controls.

### Supported Games

Here's a short list of some games Agent Smith is currently programmed to manage.

1. 7 Days To Die
2. V-Rising
3. Palworld
4. More to come!!!

# Getting Started

I've written instructions for every day use of this software as well as what a developer might need
[here](./docs/getting-started.md).

# Security

Opening a port to expose Agent Smith's API to the outside world can be a little scary, so I've
written a whole [section on it](./docs/security.md).  The author takes security very seriously, and
wants you to be informed about the risks and what's been done to make this software as safe as
possible.

# Design

There is a dedicated section regarding the [design](./docs/design.md) of Agent Smith.  For a detailed
account of system design, explanations for design choices, limitations, and more, please have a look
at that section.

# Future Work

I have identified work I intend to do for the future and could use help with.  However, if you have
an idea yourself, please create an issue for that.

There will always be room for improvements, but here are some high level goals the author has to
improve behavior and usability overall:

1. Get functional & unit test framework to minimal code coverage; 20%.
2. Cross-platform support - I'd like to be able to support Linux Distributions as well.
3. Support steam game versions; eg install latest_experiemental or a specific release.

# References / Acknowledgements

1. For packaging up and making an installer in the future - https://pyinstaller.org/en/stable/index.html
2. SteamCMD Documentation - https://developer.valvesoftware.com/wiki/SteamCMD
3. I found pythonsteamcmd here - https://github.com/f0rkz/pysteamcmd and it was helpful so I did not
   have to rebuild an interface to steamcmd.
4. All other dependencies, have a look at [requirements.txt](./requirements.txt).