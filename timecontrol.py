"""
Time control.

All times are referred to in milliseconds as per UCI protocol.
"""
import time

class TimeControl:
    def __init__(self, starttime, inc=0):
        """
        starttime is the time at start in milliseconds
            -> for different start times, use a tuple
        inc is the time added to the clock after each turn in milliseconds
            -> for different incrementations, use a tuple
        """

        #Process different start times.
        whiteTime = blackTime = None
        try:
            whiteTime, blackTime = starttime
        except TypeError:
            whiteTime = blackTime = starttime
        self.clocks = [whiteTime, blackTime]
        
        #Process different incrementation values
        whiteInc = blackInc = None
        try:
            whiteInc, blackInc = inc
        except TypeError:
            whiteInc = blackInc = inc
        self.increment = [whiteInc, blackInc]

        self._time = None
        self.turn = None # 0 for white, 1 for black.  

    def start(self, which_engine=None):
        """
        which_engine references which engine's turn it is
            0 for white, 1 for black.
        """
        self._time = time.time()

        if which_engine is None:
            if self.turn is None:
                self.turn = 0
            else:
                self.turn = -(turn-1)
        else:
            self.turn = which_engine

    def stop(self):
        """
        Stops the timer and returns whether the player's clock
        expired before the timer was stopped. (i.e. loss on time)
        """

        if self._time is None:
            raise RuntimeError("Timer was stopped before it was started.")

        time_spent = time.time() - self._time
        self._time = None

        self.clocks[self.turn] -= time_spent * 1000 # convert to ms
        if self.clocks[self.turn] < 0:
            return False

        self.clocks[self.turn] += self.increment[self.turn]
        return True
        
        
