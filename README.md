# Game Keeper (Agent)

## About

My name is Joshua and my group of friends play various games like 7 Days to Die which require one of us to host a server
at our home.  Often it's a hassle to update a server or handle restarts of a server that might have gone down.  We have
often mused over a tool that can handle this workload for us or at least make it easier.  Also, a tool that doesn't require
one of us to expose a home server to the open internet or have to require one of us to setup a home VPN. I have not found 
a very good solution that exists already so this tool might fill that vacuum.   

I am creating a solution that is a sort of two-part solution.  The first part will be what runs on someone's local machine and has the
ability to install steam apps, start/stop servers, and do other similar tasks.  There will also be a client and a minimal 
graphical user interface.  The client and the agent, shall be able to communicate securely when performed outside of one's
local network so not just anyone can interact with the agent.  

Part one (this repository) is a web api that executes commands on a machine, an agent.  The agent is supposed to be "dumb" 
in the sense that it can perform tasks, but it's only a puppet and cannot think for itself.  At a minimum, giving this 
part of the solution out allows a pair of friends to keep a game server running.  One person installs the agent at home, 
set ups the game server, and gives the other friend located elsewhere the client.  The second friend gets to remotely 
start/stop the server with the client, if needed.  Anyone, so inclined, can build additional automation around this 
part of the solution, if desired.   

For Part Two, I intend to make collaborative web application where my friends and I can control our servers via a web 
interface, and have other additional abilities.  One day, perhaps, I'll make that available to others.  

Out of all my mates, I write software for fun and this is a personal project. Help is always welcome.  If you get use
out of this tool and with to contribute back, please do.  You're welcome to use this software personally however you like.  
However, I'm licensing it such that if you take this work and use it for personal gain, then at a minimum you must 
provide any software changes you make back.  In either case, you must credit this software.

I have identified work I intend to do for the future and could use help with in the "Future Work" section.  Please create
an issue for ideas.  I also wanted to share, what I don't intend to do as well so that is also clear.

# Getting Started

I've written instructions for every day use of this software as well as what a developer might need 
[here](./docs/getting-started.md).

# Future Work

There will always be room for improvements, but here are some goals the author has to improve behavior and usability
overall:

1. Get unit test framework to minimal code coverage; 20%.
2. Add github actions.
3. Improve the usage instructions.
4. Create a simple public facing Git Hub project board. 
5. Come up with a more permanent name. 
6. Split the client into its own repository / python package. 
7. Implement authentication mechanism for client to use.
8. Implement pyinstaller so that a function EXE file can be deployed/published for releases. 
9. Cross-platform support - I'd like to be able to support Linux Game Servers as well :)

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
   so I didn't have to build the software this way, but each game has unique start up and shutdown needs.  Therefore,
   if you as a user want a game added.  Be prepared to contribute!  
2. The Graphical User Interface - To be honest, I'm not a GUI person.  It's not a pretty GUI but it gets the job done. 
   I'm not going to personally work issues to enhance the GUI, but I'm not opposed to making it better.  If someone
   wants to make it better go for it!  
3. Supporting new features so you can use this for personal gain. Again, If you do this, you must share the code back
   for the community, but I'm not going to be helping.  

# References

1. For packaging up and making an installer in the future - https://pyinstaller.org/en/stable/index.html
2. SteamCMD Documentation - https://developer.valvesoftware.com/wiki/SteamCMD

# Acknowledgements

I'm a big fan of not reinventing the wheel, and I did use some python packages that came from others.  In general,
have a look at ./requirements.txt for software I reused.

1. I found pythonsteamcmd here - https://github.com/f0rkz/pysteamcmd and it was helpful so I did not have to rebuild
   an interface to steamcmd. 