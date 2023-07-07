# Private Game Server Manager - Agent

## About

My name is Joshua and my group of friends play various games like 7 Days to Die which require one of us to host a server
at our home.  Often it's a hassle to update a server or handle restarts of a server that might have gone down.  We have
often mused over a tool that can handle this workload for us or at least make it easier.  Also, a tool that doesn't require
one of us to expose a home server to the open internet or have to require one of us to setup a home VPN. I have not found 
a very good solution that exists already so this tool might fill that vacuum.   

I am creating a solution that is a sort of two-part solution.  The first part will be what runs on someone's local machine and has the
ability to install steam apps, start/stop servers, and do other similar tasks.  There will also be a client and a minimal 
user interface.  The client and the agent, shall be able to communicate securely so not just anyone can interact with
the agent. 

The other part, this is where users get to be creative is up to you.  Part one (this repository) is a web api that executes 
commands on a machine, an agent.  The agent is supposed to be "dumb" in the sense that it can perform tasks, but it's only 
a puppet and cannot think for itself.  

Whatever controls it for whatever purpose is up to the user.  That is part two.  I intend to make part two a web application 
where my friends and I can control our individual game servers collectively and securely, and I want to keep that to myself.  
However, I think there is value in making this portion of work open to others so that is going to be publicly available in the hopes 
that others get use out of it.  

At a minimum, giving this part of the solution out allows a pair of friends to keep a game server running.  One person
installs the agent at home, set ups the game server, and gives the other friend located elsewhere the client.  The second
friend gets to remotely start/stop the server with the client, if needed.  

Out of all my mates, I write software for fun and this is a personal project. Help is always welcome.  If you get use
out of this tool and with to contribute back, please do.  You're welcome to use this software personally however you like 
and not ever bother to provide updates.  However, I'm licensing it such that if you take this work and use it for personal
gain, then at a minimum you must provide any software changes you make back.  In either case, you must credit this
software.

I have identified work I intend to do for the future and could use help with in the "Future Work" section.  Please create
an issue for ideas.

# Getting Started

I've written instructions for use of this software [here](./docs/getting-started.md).

# Future Work

There will always be room for improvements, but here are some goals the author has to improve behavior and usability
overall:

1. This is a web api meant to be use by any requestor.  Entities that call endpoints are impatient and tend to want
   a response quickly.  Right now, installing software will result in long wait times in some cases.  There needs to
   be a method to background long running tasks and report their status as a 1-100% percentage of completion.  That way
   a requestor can kick of a job, and check on how it is going.  
2. Add unit testing framework.  
3. Add github actions.
4. Improve the usage instructions.
5. Create a simple public facing Git Hub project board. 

# References

1. For packaging up and making an installer in the future - https://pyinstaller.org/en/stable/index.html
2. SteamCMD Documentation - https://developer.valvesoftware.com/wiki/SteamCMD

# Acknowledgements

I'm a big fan of not reinventing the wheel, and I did use some python packages that came from others.  In general,
have a look at ./requirements.txt for software I reused.

1. I found pythonsteamcmd here - https://github.com/f0rkz/pysteamcmd and it was helpful so I did not have to rebuild
   an interface to steamcmd. 