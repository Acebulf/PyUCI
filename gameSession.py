class GameSession:
    def __init__(self,whiteEng, blackEng, **kwargs):
        self.white = whiteEng
        self.black = blackEng
        self.gamehistory = ""
        self.write_all_engines('position startpos\n')

    def get_move(self, engine):
        engine.write('go\n')
        while True:
            for line in engine.readAll():
                if "bestmove" in line:
                    return line[9:14]
        
    def update_board(self,position):
        if "none" in position:
            return False
        self.gamehistory += " {0}".format(position)
        self.write_all_engines('position startpos moves {0}\n'
                               .format(self.gamehistory))
        return True

    def write_all_engines(self,message):
        self.white.write(message)
        self.black.write(message)

    def play(self):
        engines = [self.white,self.black]
        turn = 0
        while True:
            newmove = self.get_move(engines[turn])
            if not self.update_board(newmove):
                print self.gamehistory
                break
            turn = -(turn -1) # 0 -> 1; 1 -> 0
