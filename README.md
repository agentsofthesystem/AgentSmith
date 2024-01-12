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
3. More to come!!!

# Getting Started

I've written instructions for every day use of this software as well as what a developer might need
[here](./docs/getting-started.md).

# Security

Opening a port to expose Agent Smith's API to the outside world can be a little scary, so I've
written a whole [section on it](./docs/security.md).  The author takes security very seriously, and
wants you to be informed about the risks and what's been done to make this software as safe as
possible.

# Future Work

I have identified work I intend to do for the future and could use help with in the "Future Work"
section.  Please create an issue for ideas.  I also wanted to share, what I don't intend to do as
well so that is also clear, please see the "Author's areas of dis-interest" section for that.

There will always be room for improvements, but here are some high level goals the author has to
improve behavior and usability overall:

1. Get unit test framework to minimal code coverage; 20%.
2. Cross-platform support - I'd like to be able to support Linux Distributions as well.
3. Support steam game versions; eg install latest_experiemental or a specific release.

# Limitations

The software has some limitations that users ought to be aware of.

1. The steamcmd client that downloads a game server (based on its steam_id) does so as an anonymous user.  If it
   doesn't download publically, it's not supported very well.  The package I used addresses this but I haven't paid
   much attention to it. If your needs require authentication, be prepared for some issues.
2. Windows firewall:  This software cannot click the button that says "Allow this app through the firewall".
3. Port Forwarding: This software cannot set up port forwarding rules on any network hardware
4. Linux: To start, the agent software is intended to operate on Windows.  However, the client can run on windows or
   linux.

# Author's areas of dis-interest

In this section, the author is attempting to describe what he personally is not interested in working.

1. I want to add the games that I want to manage into the software.  I tried to go for an interface that is genearlized
   so I didn't have to build customizations for each game server.  Therefore, if you as a user want a game added.
   Be prepared to contribute!
2. The Graphical User Interface: To be honest, I'm not a GUI person.  It's not a pretty GUI but it gets the job done.
   I will help with bug-related issues, I'm not going to personally work issues to enhance the GUI unless I feel
   strongly about it.  I'm not opposed to making it better.  If someone wants to make it better go for it!
3. Supporting new features so you can use this for personal gain. Again, if you do this, you must share the code back
   for the community, but I'm not going to be helping.
4. Building any support to upload and run generic executables via API. That is a **HUGE** security risk
   I don't want this software to put on any user.

# References / Acknowledgements

1. For packaging up and making an installer in the future - https://pyinstaller.org/en/stable/index.html
2. SteamCMD Documentation - https://developer.valvesoftware.com/wiki/SteamCMD
3. All other dependencies, have a look at [requirements.txt](./requirements.txt).
4. I found pythonsteamcmd here - https://github.com/f0rkz/pysteamcmd and it was helpful so I did not
   have to rebuild an interface to steamcmd.