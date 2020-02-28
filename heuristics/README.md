# How to create an heuristic

A heuristic can be built thanks to two tools :

- A Player instance (the player playing to the game)
- A Game instance (that makes the link with the server)

It's possible to access to the positions of the humans and opponents thanks to the following methods

- get_opponent_positions() of Game
- get_humans_positions() of Game
