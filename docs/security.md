# Security

True story. While playing around with Agent Smith during development, I opened up a port and gave
it a hostname and left it running.  In the couple of days which I left it running, a bot found it
and attacked it.  My machine was compromised because I had the software running in debug mode.
After that I decided to double down on security posture.

Security with Agent Smith is handled by Nginx and by some specific settings that I've made to secure
the software:

1. First and foremost, I've disabled debug mode in the [configuration object](../application/config/config.py).
2. For the .\agent-smith.py inside of the GUI [launch.py](../application/gui/launch.py), debug mode
   is also disabled.  This script is the one that pyinstaller uses to pacakge AgentSmith for release.
3. Also, inside of [launch.py](../application/gui/launch.py), the Flask Server is set to only allow
   connections from the localhost, or 127.0.0.1.
4. Nginx handles all incoming connections.  Check out the "Security with Nginx" section below.
5. I've removed all software from AgentSmith that might be used to run any executable.  That way,
   if something was downloaded to your machine, AgentSmith won't be the mechanism that runs it.

All of that in mind, there is no reason why exposing a home server to the open internet cannot be done
safely.  Keep in mind that no matter what, your IP will be probed and tested no matter what is done.

## Best Practices

For those of us that like to tinker and change things, please watch out for the following:

1. Never ever run agent smith in debug mode and expose it to the open internet.  There is an attack
   that takes advantage of Flask's /console endpoint to run any python code.
2. Always use HTTPS/SSL to communicate outside of your home network.  If you alter the code to expose
   the Flask Server then you're taking a risk.
3. A great place to get a dynamic dns address for your home WAN is noip.com
4. Agent Smith is designed to have the ability to change the port used with Nginx.  Use one that isn't
   a standard port. Pick a random 4-5 digit number! Try to avoid commonly used port numbers.  Here
   is a wiki article on common [port numbers to avoid](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers).

I've written the code in such a way that a user must deliberately circumvent it to take the risks
I've described here.  Do so at your own risk.

### Home Network Configuration.

Our home networks are deeply personal and equally unique.  However, here are a couple of recommendations
that might help:

1. If you have a managed switch, segregate the server running agent smith onto its own VLAN.  That
   way, if it ever becomes compromised the machine is isolated from the rest of your home network.
2. Port Forwarding.  If you router supports it, specifically route the port forward to the machine
   hosting Agent Smith instead of any and all on your network.
3. If you have the ability to run an "Intrusion Protection System" then do it.  An extra set of eyes
   never hurt!

## Security with Nginx

First and formost, Nginx is a piece of software that functions as a Reverse Proxy.  That means it
takes incoming requests and routes valid request to an application secured behind itself.  In essense,
Nginx is used as a "shield" to protect API requests coming to Agent Smith from anywhere.  This section
will describe what Nginx is doing to protect you.

The following are tactics used with Nginx to secure:

1. SSL/TLS Encryption - Secures communciation so a users' token cannot be intercepted. It also
   throws off any bots looking for a simple HTTP connetion.
2. HTTPS traffic only.  Nginx actively blocks regular HTTP traffic.
3. Denies the /console route.  This prevents access to the debug route if it was accidentally
   exposed.
4. Limits the number of connetions per incoming IP address.
5. Expects the requestor to know the hostname of the server.  If you don't then the request is denied.
   This prevents bots scanning random IPs from getting through.

To see how nginx is configured, have a look at the templated [configuration file](../application/config/nginx/nginx.conf.j2).

The author is well aware that there are many more potential safeguards that Nginx might be able
to employee. If you, the reader, have a suggestion please create an Issue and help implement an
improvement!