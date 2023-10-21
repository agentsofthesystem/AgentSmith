# Getting Started

This document should contain everything a developer needs to know in order to develop and/or use this software.

## Usage

The every day user of this software may find instructions [here](./usage.md).

## Development

Development documentation can be found [here](./developer.md).

## A word about security

Flask is not a production server, ultimately.  The software does have tha ability to acept ssl certificates but how
each user obtains one is an independent venture.  Some may chose to self genreate one while others may choose to use
something else.  If communicating with this appication over HTTPS is a priority for you, then the author recommends that
the reader place this application behind a reverse proxy, such as NGINX.  

If one does use nginx, here is the windows version: https://nginx.org/en/docs/windows.html 

Why do this? It's simple, the authentication token used in this application would be directly exposed over the open 
internet over HTTP as opposed to securly with HTTPS.  One runs the risk of having someone else intercept that token and
use it for alternative purposes.
