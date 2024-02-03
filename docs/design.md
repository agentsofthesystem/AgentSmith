# Design

This section of the documentation is intended to capture how Agent Smith works, explanations for
certain design choices, limitations, and

## Architecture

Explanations regarding architecture are contained in this section.

### Generalized

In short, Agent Smith is a web server with a PyQt front end for the user.  The web server sports
an API that allows a client to make requests.  There is a go-between piece of software called,
[Operator](https://github.com/agentsofthesystem/operator), and both the PyQt GUI uses it and anyone
wishing to write their own script.  Everything is python based with the singular exception of Ningx.
For an explanation why, please see the explanations section.

### API

Application Programming Interface (API)

The api is broken into versions in the [API](../application/api/) folder.  The API itself is
versioned; v1, v2, etc...  Flask itself uses a conecpt of a "Blueprint" to break them out so each
logical section of API is broken into its own Blueprint.  For example, the games blueprint contains
the games API, and its responsible for manipulating Game Servers.

### Security

When running Agent Smith in production, the backend web server intenitally blocks outside connections
that do not come from localhost.  Incoming web connections would go through Nginx, and then are reversed
proxied back to Agent Smith.  Therefore, in production, from AgentSmith's perspective all web requests
are coming from localhost.

In reality, web requests may also come from a different IP address, so the inner software also
enforces tokenized security based on the IP address.  Nginx is configured to proxy pass the requestor's
IP address.  Whenever AgentSmith see's a request that came from an origin IP address that is not
localhost, then it will expect a valid Bearer Token.  But if the request did come from localhost,
specifically the PyQt GUI, then the backend web server will allow the connection without the token.

More about tokens.  The security tokens may be generated via the Operator client, or via GUI.  Once
the token is generated the user gets a singular chance to copy it.  The token itself is a Java Web
Token (JWT) based token.

External web requests must use SSL through Nginx and have a valid token in the request header.  The
Operator client makes this seamless to the user.

Finally, a word about flask.  Flask has a console made to run debug commands on.  That console is
intentionally disabled.  Running flask in debug mode should never be done by altering the code in
[config.py](../application/config/config.py) where "DEBUG=True".

## Game Server Framework

Game Servers are built into Agent Smith via a framework.  One will notice the [games](../application/games/)
folder contains implementations of the supported Game Servers that are available.  All of them inherit
from the [BaseGame](../application/common/game_base.py) class.

To add a new supported dedicated game server one adds a new class which implements all the abstract
functions; startup, shutdown.  The rest of the software dynamically imports the games module and
has the ability to generate the GUI on the fly.  That way someone can add a new game and not have to
worry about updating the GUI.

## Explanations

* **Why are some things implemented with Threading?** - The author is proficient in what asynchronous
  background task execution is and how that is implemented.  In python, that's typically implemented
  using a package called Celery, however, it's intentionally not being used for the purpose of keeping
  the software used to being python only.  The author wanted users to only have to download an EXE
  file and not have to install pre-requisite softare, such as a message queue server.

* **Why only supported games and not the ability to run scripts or generic executables?** - Firstly,
  security.  By not allowing scripts and generic executables to be run security is greatly enhanced.
  Next, each and every single game is different.  Some required specific arguments while others need
  an input file.  Also, some game servers don't just simply shutdown by killing the server executable,
  and need extra steps to avoid corrupting files.  Implementing a framework allows some semblance of
  order to the disorder which is the dedicated game server landscape.


## Limitations

The software has some limitations that users ought to be aware of.

1. The steamcmd client that downloads a game server (based on its steam_id) does so as an anonymous user.  If it
   doesn't download publically, it's not supported very well.  The package I used addresses this but I haven't paid
   much attention to it. If your needs require authentication, be prepared for some issues.
2. Windows firewall:  This software cannot click the button that says "Allow this app through the firewall".
3. Port Forwarding: This software cannot set up port forwarding rules on any network hardware
4. Linux: To start, the agent software is intended to operate on Windows.  However, the client can run on windows or
   linux.

## Design - Dead Ends

In this section, the author is attempting to describe both what the author personally has no interest
in working on, and "features" that Agent Smith should never adopt.  All of these items would be
considered dead ends.

### Authtor's own lack of interest

1. I want to add the games that I want to manage into the software.  I tried to go for an interface that is genearlized
   so I didn't have to build customizations for each game server.  Therefore, if you as a user want a game added that
   the author isn't crazy about playingm, then be prepared to contribute!
2. The Graphical User Interface: To be honest, I'm not a GUI person.  It's not a pretty GUI but it gets the job done.
   I will help with bug-related issues, I'm not going to personally work issues to enhance the GUI unless I feel
   strongly about it.  I'm not opposed to making it better.  If someone wants to make it better go for it!
3. Supporting new features so you can use this for personal gain. Again, if you do this, you must share the code back
   for the community, but I'm not going to be helping.

### Dead Ends

* Building any support to upload and run generic executables via API. That is a **HUGE** security
  risk I don't want this software to put on any user.
* Adding anything other than python & nginx to the tech stack.  This software is intended to be
  lean.
* By-passing security measures.  No feature reducting the security posture of this tool should be
  accepted.