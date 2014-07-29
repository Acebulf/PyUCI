"""
Example of use of GameSession and Engine to make Stockfish play itself.
"""

from gameSession import GameSession
from engine import Engine

stockfishpath = './Stockfish/src/stockfish'
eng1 = Engine(stockfishpath)
eng2 = Engine(stockfishpath)

gamesesh = GameSession(eng1,eng2).play()
