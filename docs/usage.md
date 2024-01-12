# Usage

The area of documention seeks to inform the end user the basics for using Agent Smith, and is not
intended for a developer.

## Where to get the software.

Agent Smith is automatically built and packaged each time the main branch updates.  The GitHub
releases mechanism houses the executable binary.

In a browser navigate to https://github.com/agentsofthesystem/agent-smith/releases, find the most
recent release and download "agent-smith.exe" to you machine.

TODO - Add a checksum verification method.

## How to launch the software.

Once agent-smith.exe is downloaded, move the file to a location that best suits you.  The author
recommends a place that won't change and is easily accessible, like your desktop.

Onces a suitable location, to launch the software simply double-click it to run it.  You'll be prompted
that the software is a potential threat, and you'll have to click "run anyway" to make windows run
it.

After Agent Smith has launched, a green agent icon will appear in the bottom right of your screen.
Right clicking the icon reveals the menu.

### A word about Windows.

Developer creating applications are expected to "digitally sign" executable files so that Windows
won't flag it as a potential threat.  However, to sign an executable one has to purchase an expensive
signing authority and until that expense can be covered, somehow, this warning will continue to happen.
The author's opinion is that it's sad that Windows forces you to pay or makes your software look like
a threat.

## Files and Folders Agent Smith Creates

Agent Smith creates the following directory structure:

1. games - By default games get installed into this sub-directory. The user may optionally install
           games elsewhere.
2. nginx - All things nginx go into this folder.
3. ssl - The SSL public certificate and private key are stored in this folder.
4. steam - The SteamCMD client is kept in this folder.
5. AgentSmith.db - This is an sqlite database that keeps track of everything that Agent Smith needs.

Here is how the files look on the file system:
```
C:.
├───AgentSmith
    └───games
    └───nginx
        └───nginx-<version>
    └───ssl
    └───steam
    └───AgentSmith.db
```

As of writing, Agent Smith does not have the ability to change this location or move it.

A word about the sqlite database.  Deleting this file result in Agent Smith recieving a wipe.  You'll
be back to a fresh installation.

## Instructions to install a game server

To install a supported game:

1. Right click Agent Smith's icon in the system application tray.
2. Select New Game.
3. Chose the game server you wish to install in the dropdown.
4. There will be defaults, but alter any of the installation settings as desired.
5. Click the installation button at the bottom.

## Instruction to start stop an installation.

There are two methods to quickly startup a server and shut one down.

### Using the Game Manager windows:

1. Right click Agent Smith's icon in the system application tray.
2. Select New Game.
3. Chose the game server you wish to manage in the dropdown.
4. On the bottom you can click one of Startup/Shutdown/Restart as needed.

### Using the Quick Action Menu:

Agent Smith allows the user to quickly startup or shutdown a server without going through the Game
Manager windows.

1. Right click Agent Smith's icon in the system application tray.
2. Hover your cursor over "Quck Action"
3. Click the game server you want to toggle.  If the game server is red, that means its off and clicking
   it will initiate startup.  Conversley if the game server is green, clicking it will shutdown the
   game server.

## Reporting Bugs

Things happen, don't work as expected, and many many more issues.  If it happens to you, then fill
out the bug template in GitHub [here](https://github.com/agentsofthesystem/agent-smith/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBUG%5D+%5BGUI%2C+Backend%2C+Client%5D+-+Short+Subject).

Please don't confuse feature requests with a bug... Thanks in advance!

