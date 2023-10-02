# TODO - Things to completed.

## To get to version 0.0.1

1. Add ability to update argument.
2. Add ability to delete argument. If allowed.
3. Add ability to add a new argument.
4. ~~Add ability to start/stop from game control widget.~~
5. Add ability to delete game from game control widget.
6. ~~Add ability for app/gui to work if used via pyinstaller.~~
7. Get 7DTD to work with this tool.
8. Add open source license.
9. User Testing
10. Search code for TODOs and resolve.
11. Remove code comments and random print statements.

## To get to version 0.0.2

1. Add github actions.
2. ~~Modify ./application/api/vi/game.py so that it doesn't need an enum for supported games. Instead it should search modules dynamically.  Do not want devs to have to modify this file each time a new game is added!~~
3. Finalize Documenation 
  - Add docs for how a dev can add a new game.
  - Add docs for user docs with vrising example to install/use game. 

# Nice to haves.

1. ~~Get rid of tabs on the Game control gui. Move settings under its own button on main system tray.  Get rid of summary table. Not really useful.~~ 
2. ~~Make the gui layout all nice a good looking. (Not my thing...)~~
3. Make New Game Widget size correctly.

# Other things to watch out for....

1. Things might not behave right if deleting a game.
2. Installing the same game twice?
3. ~~Errors that happen when a game is installed without any args. Edge case!~~