# TODO - Things to complete.

## To get to version 0.0.1

1. ~~Add ability to update argument.~~
2. ~~Add ability to delete argument. If allowed.~~
3. ~~Add ability to add a new argument.~~
4. ~~Add ability to start/stop from game control widget.~~
5. ~~Add ability to uninstall a game from game control widget.~~
6. ~~Add ability for app/gui to work if used via pyinstaller.~~
7. ~~Get 7DTD to work with this tool.~~
8. ~~Add open source license.~~
9. User Testing
10. Search code for TODOs and resolve.
11. ~~Remove code comments and random print statements. Except for client. Client and misc scripts can have print statements.~~
12. Add pydocs to classes, files, functions, etc...
13. Clean up imports in all files.
14. Clean up typing hints in all files.
15. ~~Implement Alembic revisions.~~
16. ~~Add default values to New Game Gui.~~

## To get to version 0.1.0  (First minor release)

1. Add github actions.
2. ~~Modify ./application/api/vi/game.py so that it doesn't need an enum for supported games. Instead it should search modules dynamically.  Do not want devs to have to modify this file each time a new game is added!~~
3. Finalize Documenation 
  - Add docs for how a dev can add a new game.
  - Add docs for user docs with vrising example to install/use game. 
  - Add docs about app version schema.
4. Turn off auto updates on Game Manager window when its closed.
5. ~~Add github issue template.~~
6. Add ability to designate which port the flask app runs on in settings.
7. Add ability to designate where the database file is saved.
8. Add a game update button, so someone can update a game server.  
9. Upate the client such that it is a python package in and of itself.

## To get to version 1.0.0 (First major release)
1. Some sort of upgrade ability; eg if a new version of the app comes out, it'll show up in settings or user can
   click "check for updates somewhere."

# Nice to haves.

1. ~~Get rid of tabs on the Game control gui. Move settings under its own button on main system tray.  Get rid of summary table. Not really useful.~~ 
2. ~~Make the gui layout all nice a good looking. (Not my thing...)~~
3. ~~Make New Game Widget size correctly.~~

# Other things to watch out for....

1. ~~Things might not behave right if deleting a game.~~
2. What happens if I install the same game twice?
3. ~~Errors that happen when a game is installed without any args. Edge case!~~
4. Having two games installed and uninstalling one of them. Not sure how game manager GUI will react.
5. Add mypy to github actions.
6. Github actions builds pyinstaller as linux executable, not windows. Need to explore how to make it a windows exe.
7. When installing a game server, there's no way to specify which version of it.  The downloader assumes the user wants
   the most recent release available on steam.
8. Some games, may not need to allow the user to add arguments.  Need to have a way to disable that.

# Bugs

1. ~~Changing between games on the Game Manager Gui doesn't work.~~
2. Argument table on New Games windows does not resize properly.
3. ~~Quick Start/Stop GUI doesn't index properly. If I click to start vrising... 7dtd starts. etc..~~
4. ~~Changing between games on new game widget breaks the gui.~~