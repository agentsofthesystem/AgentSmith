# Testing

Testing an application is imperative as it grows because as new features and fixes are introduced,
the potential for creating more issues than get solved increases.

## Test Plan

The goal is to first, implement unit testing and then system testing with the PyQt GUI.  In the end,
all testing (or as much as possible) should become a part of CI/CD checks.

A word about code coverage - In my experience people associate code coverage with an in-fallable
system.  That is, if the code coverage is 95% then the system cannot have any bugs in it, certainly!
The author disagrees with this mentality.  Instead, the author belives its best to use code coverage
metrics as a guidline and instead focus on test case coverage.   In a perfect world, test driven
development would drive test case coverage, but in reality code gets written and tests are added
both as one can plan for and as issues are found.

### Desired Unit Testing

1. Testing API Endpoints.
2. Testing the Token authentication mechanisms.
3. Testing all isolated functions.

### Desired System Testing

1. Testing that the GUI can install a game server properly.
2. Testing that the GUI can startup, shutdown and restart an installed game server properly.
3. Testing that the GUI can update a game server properly.
4. Testing that the GUI can uninstall a game server.
5. Testing that installing a new game results in the quick action menu being updated.
6. Testing that uninstalling a game results in the quick action menu being updated.

### Other testing.

Other testing might consist of load testing, erroneous input testing, fault testing which is to mean
intentionally causing an error, and much more.

Ideas:

1. Try to break API endpoints with usupported HTTP request types and inputs.
2. Run game servers for days on end and then check basic functionality.
3. Try to do odd things like uninstall a game while its running or delete a database record and see
   how the system reacts.