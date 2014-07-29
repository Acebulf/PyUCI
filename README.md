PyUCI
=====

The Python UCI Chess Engine Interface (PUCEI or PyUCI) allows communication with a UCI-enabled chess engine from Python 2.x on Unix-based machines.

In very early stages of development.

For an example of use see rungame.py (making an engine play itself.) 

Here is an example where we make Stockfish play itself: (see rungame.py)

```Python
from gameSession import GameSession
from engine import Engine

stockfishpath = './Stockfish/src/stockfish'
eng1 = Engine(stockfishpath)
eng2 = Engine(stockfishpath)

gamesesh = GameSession(eng1,eng2).play()
```
    
TODO:

* Complete option integration at initialization in engine.py.
* Add non-Unix support.
* Documentation

(... more stuff)
