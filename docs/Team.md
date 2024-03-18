# Team Methods

Since these are methods of the `Team` class, you will need to call them using dot notation on a member of this class, that is a variable that is expected to be a `Team`, like the parameter of `ActTeam`.

For example:
```py
def def ActTeam(team):
    # Try building walls on all islands
    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)
```

## Actions

### `buildWalls(island_number) -> bool`
Attempt to build a wall on the island corresponding to the given island number (`1`, `2` or `3`). Will succeed only if: 
- The team has the required resources (<u>i.e.</u> 100 Wood)
- The team is the only team present on the island
- The cooldown is complete 

The cooldown is of `X` frames between the last wall breaking and the next wall being built.

## Signalling

### `getTeamSignal() -> str`
Returns the current signal of the team.

### `setTeamSignal(sig)`
Sets the signal of the pirate's team to `sig` if `sig` is a string and its length is less than or equal to 100.

### `getListOfSignals() -> str[]`
Returns a list containing the signals of all the pirates in the team.
This list is **read-only**, changing signals in the array will not change it for the pirate.

## Info

### `trackPlayers() -> str[]`
Returns a list of length 6, containing info on the current status of all the islands.

The first three items correspond to the occupation of Island 1, 2 and 3 respectively by the team, and can take values `''`, `'myCapturing'` and `'myCaptured'`.

The last three items correspond to the occupation of Island 1, 2 and 3 respectively by other team, and can take values `''`, `'oppCapturing'` and `'oppCaptured'`.

Example:
```py
# All islands have been taken by opponent
team.trackPlayers() # ['','','','oppCaptured','oppCaptured','oppCaptured']

# Island 1 is yours, Island 2 is the opponent's but you are currently trying to capture it
team.trackPlayers() # ['myCaptured','myCapturing','','','oppCaptured','']
```

### `getTotalPirates()`
Returns the total number of pirates the team has.

### `getTotalRum()`
Returns the total amount of rum the team has.

### `getTotalGunpowder()`
Returns the total amount of gunpowder the team has.

### `getTotalWood()`
Returns the total amount of wood the team has.

### `getDeployPoint()`
Returns the position at which the team spawns pirates as a tuple `(x, y)`. 

### `getDimensionX()`
Returns the X dimension of the game.

### `getDimensionY()`
Returns the Y dimension of the game.

### `buildWalls(island_no)`
Builds walls around the specified island. Does nothing if the team does not have enough wood to build walls.

### `getCurrentFrame()`
Returns the current time frame of the game