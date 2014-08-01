"""
Time control.

All times are referred to in milliseconds as per UCI protocol, unless
time_modifier kwarg is used.
"""
import time

class TimeControl:
    def __init__(self, starttime, inc=0, **kwargs):
        """
        starttime is the time at start in milliseconds
            -> for different start times, use a tuple
        inc is the time added to the clock after each turn in milliseconds
            -> for different incrementations, use a tuple

        'time_unit' is a kwarg which allows starttime and inc to use units
        different from milliseconds.
           -> 'min' for minutes. (values passed will be multiplied by 60 000)
           -> 'sec' for seconds  (values passed will be multiplied by 1 000)
           -> 'minsec' to use minutes for starttime and seconds for inc.
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

        #Process time_modifier
        if 'time_unit' in kwargs:
            st_mod = inc_mod = 1
            if kwargs['time_unit'] == 'min':
                st_mod = inc_mod = 60000 #60 seconds = 60k milliseconds
            elif kwargs['time_unit'] == 'sec':
                st_mod = inc_mod = 1000 #1 second
            elif kwargs['time_unit'] == 'minsec':
                st_mod = 60000
                inc_mod = 1000
            else:
                raise ValueError("Argument for time_unit is invalid")
            
            self.clocks = [x * st_mod for x in self.clocks]
            self.increment = [x * inc_mod for x in self.increment]

        #Turn and time variables initialization
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
        
        
