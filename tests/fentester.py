from fenparser import FENOperator as FEN
testnumber = 0

def testing (fen, out):
    global testnumber
    testnumber += 1
    print testnumber
    assert((str(fen) == str(fen)))
    print str(fen)
    print out
    assert(str(fen) == out)
    print '-'*10

#1. En passant check
test = FEN('rnbqkbnr/ppp1pp1p/8/3p2p1/4P1P1/8/PPPP1P1P/RNBQKBNR w KQkq g6 0 3')
test.do_move('c2c4')
output = 'rnbqkbnr/ppp1pp1p/8/3p2p1/2P1P1P1/8/PP1P1P1P/RNBQKBNR b KQkq c3 0 3'
testing(test,output)

#2. Moving white king prevents castling
test = FEN('rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq d6 0 4')
test.do_move('e1e2')
output = 'rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPPKPPP/RNBQ3R b kq - 1 4'
testing(test,output)

#3. Moving king-side white rook prevents king-side castling.
test = FEN('rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq d6 0 4')
test.do_move('h1g1')
output = 'rnbqkb1r/ppp2ppp/5n2/3pp3/2B1P3/5N2/PPPP1PPP/RNBQK1R1 b Qkq - 1 4'
testing(test,output)

#4. Moving queen-side white rook prevents queen-side castling.
test = FEN('rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/b4N2/1PPP1PPP/RNBQK1R1 w Qkq - 1 6')
test.do_move('a1a3')
output = 'rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 b kq - 0 6'
testing(test,output)

#5. Moving black king prevents castling

test = FEN('rnbqk2r/ppp2ppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 b kq - 0 2')
test.do_move('e8e7')
output = 'rnbq3r/ppp1kppp/5n2/4p3/P1BpP3/R4N2/1PPP1PPP/1NBQK1R1 w - - 1 3'
testing(test,output)

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
