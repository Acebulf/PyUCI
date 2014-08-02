"""
Python FEN Operator developed as part of the PUCEI (PyUCI) project. 
"""

class FENOperator:
    def __init__(self,_FEN):
        self.FEN = _FEN

        #Allow starting the fen with 'startpos'
        if self.FEN == 'startpos':
            self.FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        #Split into its base components
        FENSplit = self.FEN.split(' ') 

        boardFEN = FENSplit[0]
        self.turn = FENSplit[1] #Active Color; w for white, b for black
        self.castling = FENSplit[2] #Castling position
        self.ep = FENSplit[3] #En passant
        self.cp_clock = FENSplit[4] #Capture/Pawn movement clock in halfmoves
        self.moves = FENSplit[5] #Number of moves

        #Parsing the FEN
        self.board = self.FEN_to_Board(boardFEN)
        

            
    def FEN_to_Board(self, boardFEN):

        #Replace numbers by an equivalent number of spaces.
        for x in xrange(1,9):
            boardFEN = boardFEN.replace(str(x),' '*x)

        #Split each line
        boardFEN = boardFEN.split('/')
        
        #Split into individual characters and reverse
        boardFEN = [list(x) for x in boardFEN]
        boardFEN.reverse()

        return boardFEN

    def outputFEN(self, positionOnly=False):
        boardFEN = list(self.board)
        boardFEN.reverse()
        boardStr = ''
        for line in boardFEN:
            for x in line:
                boardStr += x
            boardStr += '/'
        boardStr = boardStr[:-1] #remove trailing /
        for x in xrange(8,0,-1):
            boardStr = boardStr.replace(' '*x, str(x))
        
        if self.castling == '':
            self.castling = '-'

        if positionOnly: #Return a shorter version for tie checking
            return '{0} {1} {2}'.format(boardStr,self.turn,self.castling)

        return '{0} {1} {2} {3} {4} {5}'.format(boardStr, self.turn,
                                                self.castling, self.ep,
                                                self.cp_clock, self.moves)

    
    def coordinates(self, pos):
        #Turn a positional string (e.g. e4) into array coordinates
        return int(pos[1]) - 1, 'abcdefgh'.index(pos[0])

    def to_string(self, coords):
        #Turn array coordinates into a string.
        number = coords[0] + 1
        letter = 'abcdefgh'[coords[1]]
        return str(letter)+str(number)

    def do_move(self, move):
        """
        Move is string represented in UCI algebric notation (e.g. e2e4, e7e8q)
        """
        move = move.replace(' ','') #Remove spaces

        from_coords = self.coordinates(move[0:2])
        to_coords = self.coordinates(move[2:4])

        #Check for promotion
        if len(move) == 5:
            promotion = move[4]
            if self.turn == 'w':
                promotion = promotion.upper()
        else:
            promotion = None

        piece = self.board[from_coords[0]][from_coords[1]]

        #Reset cp_clock if piece is being captured or pawn is moved.
        if self.board[to_coords[0]][to_coords[1]] != ' ' or piece in 'pP':
            self.cp_clock = 0
        else:
            self.cp_clock = str(int(self.cp_clock) + 1)

        
        #Move piece to new position and remove piece at old position.
        if promotion is None:
            self.board[to_coords[0]][to_coords[1]] = piece 
        else:
            self.board[to_coords[0]][to_coords[1]] = promotion
        self.board[from_coords[0]][from_coords[1]] = ' '

        #Check for castling and move rook if necessary.
        if piece in 'kK':
            if move == 'e1g1': #king-side white castling
                self.board[0][7] = ' '
                self.board[0][5] = 'R'
            elif move == 'e1c1':#queen-side white castling
                self.board[0][0] = ' '
                self.board[0][3] = 'R'
            elif move == 'e8g8':#king-side black castling
                self.board[7][7] = ' '
                self.board[7][5] = 'r'
            elif move == 'e8c8':#queen-side black castling
                self.board[7][0] = ' '
                self.board[7][3] = 'r'
            
        #Removing castling rights if king is moved.
        if piece == 'k':
            self.castling = self.castling.replace('k','').replace('q','')
        elif piece == 'K':
            self.castling = self.castling.replace('K','').replace('Q','')
        
        #Removing castling rights if rook is moved.
        if piece == 'r':
            if from_coords == (7,7):
                self.castling = self.castling.replace('k','')
            elif from_coords == (7,0): 
                self.castling = self.castling.replace('q','')
        if piece == 'R':
            if from_coords == (0,7):
                self.castling = self.castling.replace('K','')
            elif from_coords == (0,0):
                self.castling = self.castling.replace('Q','')

        #En passant
        if from_coords[0] == 1 and to_coords[0] == 3 and piece == 'P':
            self.ep = self.to_string((2,from_coords[1]))
        elif from_coords[0] == 6 and to_coords[0] == 4 and piece == 'p':
            self.ep = self.to_string((5,from_coords[1]))
        else:
            self.ep = '-'

        #Increment moves counter if move is done by black
        if self.turn == 'b':
            self.turn = 'w'
            self.moves = str(int(self.moves)+1)
        else:
            self.turn = 'b'
        
    def __str__(self):
        return self.outputFEN()

    def getPositionOnly(self):
        return self.outputFEN(True) #positionOnly = True

        
