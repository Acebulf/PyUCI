"""
Example of use of GameSession and Engine to make Stockfish play itself.
"""

from gameSession import GameSession
from engine import Engine

stockfishpath = './stockfish_8_x64'
eng1 = Engine(stockfishpath)
eng2 = Engine(stockfishpath)

#GameSession(eng1,eng2).play()
GameSession(eng1,eng2,time=(300e3,5e3)).play()
