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

All supported games can be found [here](https://docs.agentsofthesystem.com/build/html/agent_smith/supported-game-servers.html).

# Getting Started

To learn how to use Agent Smith please read the [User Guide](https://docs.agentsofthesystem.com/build/html/agent_smith/usage.html)

# Security

Security is a big deal, the author wrote a whole section about it. Have a look at the
[Security Docs](https://docs.agentsofthesystem.com/build/html/agent_smith/security.html).

# References / Acknowledgements

1. For packaging up and making an installer in the future - https://pyinstaller.org/en/stable/index.html
2. SteamCMD Documentation - https://developer.valvesoftware.com/wiki/SteamCMD
3. I found pythonsteamcmd here - https://github.com/f0rkz/pysteamcmd and it was helpful so I did not
   have to rebuild an interface to steamcmd.
4. All other dependencies, have a look at [requirements.txt](./requirements.txt).
