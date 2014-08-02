from fenoperator import FENOperator as FEN
from sys import argv

if '-silent' in argv or '-s' in argv:
    silentmode = True
else:
    silentmode = False

testnumber = 0

def testing (fen, out):
    global testnumber
    testnumber += 1
    if not silentmode:
        print testnumber
        print str(fen)
        print out
        print '-'*10
    assert((str(fen) == str(fen)))
    assert(str(fen) == out)


#1. startpos compliance.
test = FEN('startpos')
output = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
testing(test,output)

#2. En passant check
test = FEN('rnbqkbnr/ppp1pp1p/8/3p2p1/4P1P1/8/PPPP1P1P/RNBQKBNR w KQkq g6 0 3')
test.do_move('c2c4')
output = 'rnbqkbnr/ppp1pp1p/8/3p2p1/2P1P1P1/8/PP1P1P1P/RNBQKBNR b KQkq c3 0 3'
testing(test,output)

#3. Moving white king prevents castling
test = FEN('rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq d6 0 4')
test.do_move('e1e2')
output = 'rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPPKPPP/RNBQ3R b kq - 1 4'
testing(test,output)

#4. Moving king-side white rook prevents king-side castling.
test = FEN('rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq d6 0 4')
test.do_move('h1g1')
output = 'rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPP1PPP/RNBQK1R1 b Qkq - 1 4'
testing(test,output)

#5. Moving queen-side white rook prevents queen-side castling.
test = FEN('rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/b4N2/1PPP1PPP/RNBQK1R1 w Qkq - 1 6')
test.do_move('a1a3')
output = 'rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 b kq - 0 6'
testing(test,output)

#6. Moving black king prevents castling
test = FEN('rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 b kq - 0 2')
test.do_move('e8e7')
output = 'rnbq3r/ppp1kppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 w - - 1 3'
testing(test,output)

#7. Checking castling (king-side white) + adding spaces to move input
test = FEN('rnbqk1nr/pppp2pp/3b1p2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4')
test.do_move('e1g1   ')
output = 'rnbqk1nr/pppp2pp/3b1p2/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 1 4'
testing(test,output)

#8. Castling (queen-side white)
test = FEN('rnbq1knr/p1p3pp/5p2/1p1pp3/2B1P3/NPP2N2/P2PQPPP/R3K2R w KQ d6 0 10')
test.do_move('e1c1')
output = 'rnbq1knr/p1p3pp/5p2/1p1pp3/2B1P3/NPP2N2/P2PQPPP/2KR3R b - - 1 10'
testing(test,output)

#9. Series of moves
test = FEN('rnbq1knr/p1p3pp/5p2/1p1pp3/2B1P3/NPP2N2/P2PQPPP/2KR3R b - - 1 10')
test.do_move('d5e4')
test.do_move('d2d3')
test.do_move('e4f3')
test.do_move('h2h3')
test.do_move('f3g2')
test.do_move('f2f3')
testing(test,'rnbq1knr/p1p3pp/5p2/1p2p3/2B5/NPPP1P1P/P3Q1p1/2KR3R b - - 0 13')
#10. Promotion
test.do_move('g2h1q')
testing(test,'rnbq1knr/p1p3pp/5p2/1p2p3/2B5/NPPP1P1P/P3Q3/2KR3q w - - 0 14')

#Barrage of moves
test = FEN('rnbqkb1r/ppp2ppp/5n2/4p3/P1BpP3/5N2/1PPP1PPP/RNBQK1R1 b Qkq a3 0 5')
test.do_move('f8a3')
testing(test,'rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/b4N2/1PPP1PPP/RNBQK1R1 w Qkq - 1 6')
test.do_move('a1a3')
testing(test,'rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 b kq - 0 6')
test.do_move('a7a5')
testing(test,'rnbqk2r/1pp2ppp/5n2/p3p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 w kq a6 0 7')
test.do_move('f3e5')
testing(test,'rnbqk2r/1pp2ppp/5n2/p3N3/P1BpP3/R7/1PPP1PPP/1NBQK1R1 b kq - 0 7')

print ('FENOperator tests successful.')
