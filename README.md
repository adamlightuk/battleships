# battleships

To play, you need cryptography and pillow packages. As well as Python insalled


Run the following in a terminal

pip install cryptography
<p>
pip install pillow

Line 305 has a path to the icon folder found on this github
Download the icon folder and copy the file path to line 305 in place of the current path.
Python needs slashes to be forward slashes(/) not backslashes(\). You may need to change this manually.
<p>
<B>Marking criteria for the implementation of the Battleship game</B>

<B>Achieving a mark of 40% to maximum of 49%
The game must implement all the following:</B>

  • Two players have two grids.
  
  • Each player can secretly position the ships on its primary grid

   • Each ship can position 5 types of ships either horizontally or vertically on the grid

  • Players take turns to target opponent's grid. If hit the grid changes its colour to red,
  otherwise it turns to white for miss.

  • When a player hits a hidden ship, the player is given an extra turn until it is a miss.

  • Text based user interface is used to play the game.

  • Computer player plays randomly.

<B>Achieving a mark of 50% to maximum of 59%
The game must implement all the above and the following:</B>

  • Development of Basic Graphical User Interface (GUI) using Python Tkinter.

  • The game should announce the losing player and type of ship that was sunk.

  • The game should announce the winning player when all opponent’s ships have sunk.

  • Computer player should allow some time before it target opponent’s grid. 2 seconds,
  emulating its thinking period even if the next move is random.

<B>Achieving a mark of 60% to maximum of 69%
The game must implement all the above and the following:</B>

  • Players can select the size of the grid at the beginning of the game.

  • The game must validate the positions of the ships. For example, the ships cannot overlap
  (i.e., only one ship can occupy any given square in the grid).

  • Ships should only be placed within the game grid.

  • The game can be saved and loaded into and from a text file.

<B>Achieving a mark of 70% to maximum of 79%
The game must implement all the above and the following:</B>

  • Computer player uses random moves, but when there is a hit, it should continue hitting the
  ship by hitting adjacent grids laid horizontally or vertically on the grid.

  • Computer player should consider the type of ship and its size when implement the above
  functionalities.

<B>Achieving a mark of 80% and over
The game must implement all the above and the following:</B>

  • Computer player should exhibit some intelligence. For example, learning from its previous
  moves when targeting new grids.
