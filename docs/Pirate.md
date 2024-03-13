# Pirate Methods

Since these are methods of the `Pirate` class, you will need to call them using dot notation on a member of this class, that is a variable that is expected to be a `Pirate`, like the parameter of `ActPirate`.

For example:
```py
def ActPirate(pirate):
    # If there is no wall above, move upward
    if pirate.investigate_up() != "wall":
        return 1; # Up
    else:
        return 0; # No movement
```

## Investigation

A pirate is able to investigate all 8 tiles surrounding it, by which it can find out what lies in those tiles.
Tiles are referred to based on their direction with respect to the pirate.

![The names used to refer to the tiles adjacent to the pirate](/docs/media/directions.jpg)

- **`investigate_current_position()`** : This function is used to investigate the current location of the pirate.

- **`investigate_up()`** : This function is used to investigate the area above the current location of the pirate.

- **`investigate_left()`** : This function is used to investigate the area to the left of the current location of the pirate.

- **`investigate_down()`** : This function is used to investigate the area below the current location of the pirate.

- **`investigate_right()`** : This function is used to investigate the area to the right of the current location of the pirate.

- **`investigate_ne()`** : This function is used to investigate the area in the northeast direction of the current location of the pirate.

- **`investigate_nw()`** : This function is used to investigate the area in the northwest direction of the current location of the pirate.

- **`investigate_se()`** : This function is used to investigate the area in the southeast direction of the current location of the pirate.

- **`investigate_sw()`** : This function is used to investigate the area in the southwest direction of the current location of the pirate.

Each of the above functions returns one of the following strings, corresponding to the contents of the investigated tile: 
- ***'wall'*** if the tile is out of bounds
- ***'friend'*** if a ship from the same team is on the tile
- ***'enemy'*** if a ship from the other team is on the tile
- ***'island1', 'island2' or 'island3'*** if the tile is a part of an island
- ***'blank'*** in all other cases

## Info

### `getTotalRum()`
Returns the total amount of rum the team has.

### `getTotalGunpowder()`
Returns the total amount of gunpowder the team has.

### `getTotalWood()`
Returns the total amount of wood the team has.

### `getPosition()`
Returns the position of the pirate as a tuple `(x, y)`. 

### `getDeployPoint()`
Returns the coordinates of the deploy point of the team as a tuple `(x, y)`.

### `getDimensionX()`
Returns the X dimension of the game.

### `getDimensionY()`
Returns the Y dimension of the game.

## Signalling

### `GetInitialSignal()`
Returns the initial signal of the pirate.

### `getSignal()`
Returns the current signal of the pirate.

### `setSignal(sig)`
Sets the signal of the pirate to `sig` if `sig` is a string and its length is less than or equal to 20.

### `getTeamSignal()`
Returns the current signal of the team.

### `setTeamSignal(sig)`
Sets the signal of the pirate's team to `sig` if `sig` is a string and its length is less than or equal to 20.

### `getListofTeamSignals() -> str[]`
Returns a list containing the signals of all the pirates in the team.
This list is **read-only**, changing signals in the array will not change it for the pirate.

### `trackPlayers()`
Returns a list of length 6, containing info on the current status of all the islands.

The first three items correspond to the occupation of Island 1, 2 and 3 respectively by the pirate's team, and can take values `''`, `'myCapturing'` and `'myCaptured'`.

The last three items correspond to the occupation of Island 1, 2 and 3 respectively by other team, and can take values `''`, `'oppCapturing'` and `'oppCaptured'`.

Example:
```py
# All islands have been taken by opponent
pirate.trackPLayers() # ['','','','oppCaptured','oppCaptured','oppCaptured']

# Island 1 is yours, Island 2 is the opponent's but you are currently trying to capture it
pirate.trackPlayers() # ['myCaptured','myCapturing','','','oppCaptured','']
```

### `getCurrentFrame()`
Returns the current time frame of the game