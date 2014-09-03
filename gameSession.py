from timecontrol import TimeControl
from fenoperator import FENOperator

class GameSession:
    def __init__(self,whiteEng, blackEng, **kwargs):
        """
        The basic GameSession class.
        whiteEng and blackEng are the two engines, with respective colors

        Note: All times are in milliseconds as per UCI protocol, unless
        time_modifier (see the TimeControl class) is used.

        start_time is the time that the engines are given on the clock,
        not including this parameter will result in an untimed game. A tuple
        can be fed to allow different starting times like so:
        start_time = (<white start time>,<black start time>)

        inc is the incremented time value after each turn. Like start_time,
        it can be fed a tuple for different incrementations to each engine.

        time is a tuple that combines start_time and inc 
        in the following format: time=(start_time,inc).

        If time is a single number (int, float, etc.), the value it is passed
        will be considered as start_time, and inc as 0.

        The position keyword argument is used to pass a FEN value as the starting position,
        when not used, the default starting position (startpos) is used.
        """

        self.white = whiteEng
        self.black = blackEng
        self.gamehistory = ""
        self.timed = False

        self.tied = False
        self.tiereason = ''
        self.winner = None

        #Process TimeControl Arguments
        tc_dict = {}
            #Pass any argument in tc_dict to time control.
        if 'tc_dict' in kwargs:
            tc_dict.update(kwargs['tc_dict'])
        if 'time_unit' in kwargs:
            tc_dict['time_unit'] = kwargs['time_unit']
            

        if 'time' in kwargs:
            self.timeControl = TimeControl(*kwargs['time'], **tc_dict)
            self.timed = True
        elif 'start_time' in kwargs:
            inc = 0
            if 'inc' in kwargs:
                inc = kwargs['inc']
            self.timeControl = TimeControl(kwargs['start_time'],inc, **tc_dict)
            self.timed = True

        starting_position = 'startpos'
        if 'position' in kwargs:
            starting_position = kwargs['position']
        
        
        #Tie testing (repeated moves)
        self.played_positions = {}
        self.FENOp = FENOperator(starting_position)
        self.played_positions[self.FENOp.getPositionOnly()] = 1
        self.write_all_engines('position fen {0}\n'.format(self.FENOp))

    def get_move(self, engine):
        command = 'go'
        
        if self.timed:
            wtime, btime = self.timeControl.clocks
            winc, binc = self.timeControl.increment
            command += ' wtime {0} btime {1} winc {2} binc {3}'
            command = command.format(wtime, btime, winc, binc)
        
        engine.write('{0}\n'.format(command))
        while True:
            for line in engine.readAll():
                if "bestmove" in line:
                    return line[9:14]
        
    def update_board(self,position):
        if "none" in position:
            return False
        self.tied = self.check_tie(position) #Also updates FENOperator
        self.gamehistory += " {0}".format(position)
        self.write_all_engines('position fen {0}\n'.format(self.FENOp))
        return True

    def write_all_engines(self,message):
        self.white.write(message)
        self.black.write(message)

    def play(self):
        engines = [self.white,self.black]
        turn = 0
        while True:
            if self.timed:
                self.timeControl.start(turn)

            newmove = self.get_move(engines[turn])
            if not self.update_board(newmove):
                print self.gamehistory
                if turn == 1:
                    print "White checkmates"
                else:
                    print "Black checkmates"
                break

            if self.tied:
                print self.gamehistory
                print "Draw by {0}".format(self.tiereason)
                break

            # Check for time
            if self.timed:
                if not self.timeControl.stop():
                    print self.gamehistory

                    #Print "loses on time" message.
                    if turn == 0:
                        print "White loses on time"
                    else:
                        print "Black loses on time"
                    break
                        
            turn = -(turn -1) # 0 -> 1; 1 -> 0

    def check_tie(self, move):
        """
        Checks for tie and updates FENOperator
        """
        if self.white.score == 0 and self.black.score == 0:
            return True

        self.FENOp.do_move(move)
        newstr = self.FENOp.getPositionOnly()
        
        if newstr in self.played_positions:
            self.played_positions[newstr] += 1
            if self.played_positions[newstr] >= 3:
                self.tiereason = '3 move repeat'
                return True
        else:
            self.played_positions[newstr] = 1

        if int(self.FENOp.cp_clock) >= 100:
            self.tiereason = '50 moves without capture or pawn moving'
            return True
        
        return False
