# Components
1. [Map](#map)
2. [Team](#team)
3. [Resources](#resources)
4. [Islands](#islands)
5. [Pirates](#pirates)


## Map

The Map is a randomly generated square grid of tiles (typically `40 x 40`), that contain 3 islands of size `3 x 3`, and collectible resources scattered across most of the remaining tiles.

The islands are spawned such that on symmetrically dividing the map into 4 quadrants, 3 of them have islands. The two opposite corners of the map in quadrants with islands are chosen, and set as the deploy points for each team's pirates (the location where new pirates are spawned). 

<img src="./media/screenshot.jpg" width="360" height="360" />

> _A screenshot of the Map mid-game, with lines drawn to show the 4 quadrants_

Whenever a pirate (or pirates) land on a tile with a resource, it gets distributed between both teams depending on the proportion of pirates present at that spot, and the resource is exhausted.

Most of these resources are not replenished (see [Resources](#resources)).

## Team

There are two teams in the game: **Red** and **Blue**

At the start of the team, both of the two teams are provided with `X` Rum, `X` Wood and `X` Gunpowder. Each team is also assigned one deploy point (see [Map](#map)).



## Resources

There are 3 resources that you will find scattered the map. Resources are collected by a team when their pirates move onto tiles that contain them. These resources are **shared commonly by the whole team**, and play different roles in the game:

### Rum
Rum is used to spawn more pirates at the team's deploy point. It is used automatically on collection, and each pirate costs `50` Rum. 

Rum is never replenished, and is thus a limited resource on the Map.

### Wood
Wood is used to build walls around islands the team is occupying. Building walls costs `50` Wood, and the team must decide when to use this resource. 

When walls are built around an island, pirates within the walls cannot leave the island and pirates from outside cannot enter the island. A team can build walls around an island only if there are no enemy pirates in that island.

Walls around an island are automatically dissolved after `50` timeframes.

Each island also has a cooldown period of `35` timeframes, during which walls cannot be built around it.

Wood is never replenished, and is thus a limited resource on the Map.

### Gunpowder
Gunpowder is an important resource used in battles, when pirates come in contact with each other <u>i.e.</u> move onto the same tile.

If the pirate's team has atleast `100` Gunpowder, then the pirate destroys the enemy pirate.

More specifically, if both teams have atleast `100` gunpowder, both pirates are killed. If only one team has atleast `100` gunpowder, only the enemy pirate is killed. If both teams have less than `100` gunpowder, neither pirate is killed.

Gunpowder is periodically replenished on the Map if its amount falls below a certain threshold.

## Islands
![All the 3 islands in the game](./media/flags.png "All the 3 islands in the game")
## Pirates

Pirates are the functional units of a team, that explore the map, collect resources and capture islands.

The primary action that a pirate can perform is to **move**, and to decide where to move it can investigate its surroundings and communicate with its team via signals.

Each pirate occupies exactly one tile at any time, and any tile that has one or more pirates from a team will have a ship displayed on it.

## Communication Between Team and Pirates

There are three types of Signals in the game:

1. Those passed onto Robots, when they are created (by the Team)
2. Those which are put up by the team and can be read by all of its pirates
3. Those which are put up by pirates and can be read by the parent team

These can be used to co-ordinate movements and strategize attacks/defence.
