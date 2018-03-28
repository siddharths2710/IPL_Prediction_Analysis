IPL data in CSV format
======================

The background
--------------

This data was obtained from the scraping using a quick Python script, and is
attributed to Stephen (email:  stephen[at]cricsheet[dot]org)



The format of the data
----------------------

Each file has a 'version', multiple 'info' lines, and multiple 'ball' lines.
'version' is just 1 for now. The 'info' entries should be fairly self-explanatory.

Each 'ball' line has the following fields:

  * The word 'ball' to identify it as such
  * Innings number, starting from 1
  * Over and ball
  * Batting team name
  * Batsman
  * Non-striker
  * Bowler
  * Runs-off-bat
  * Extras
  * Kind of wicket, if any
  * Dismissed played, if there was a wicket

