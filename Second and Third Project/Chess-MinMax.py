import chess

# 1) Vlerat e figurave (mund t’i ndryshoni sipas dëshirës)
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100  # Zakonisht mbretit i jepet një vlerë e lartë, edhe pse loja mbaron nëse kapet mbreti.
}

def evaluate_board(board: chess.Board) -> int:
    """
    Një funksion i thjeshtë vlerësimi:
      - Mbledh vlerat e figurave nga perspektiva e lojtarit që është në radhë (board.turn)
      - Zbrit vlerat e figurave të kundërshtarit
      - Opsionale: mund të shtojmë edhe një term “lëvizshmërie”: diferencën në numrin e lëvizjeve të ligjshme
    """
    if board.is_game_over():
        # Nëse loja ka mbaruar, shikojmë nëse është shah-mat apo barazim
        if board.is_checkmate():
            # Nëse është shah-mat, humb lojtari që është në radhë
            return -9999  # vlerë e madhe negative nëse ky lojtar është i matuar
        else:
            # Barazim (stalemate) ose ndonjë tjetër
            return 0

    # Do të mbledhim një rezultat.
    # Pozitiv do të thotë më e favorshme për lojtarin në radhë (board.turn).
    # Negativ do të thotë më e favorshme për kundërshtarin.
    material_score = 0
    
    # Kalojmë nëpër çdo katror të tabelës
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            # Shtojmë vlerën nëse është e lojtarit që lëviz, heqim nëse është e kundërshtarit
            value = PIECE_VALUES.get(piece.piece_type, 0)
            if piece.color == board.turn:
                material_score += value
            else:
                material_score -= value

    # “Mobility” e thjeshtë: diferenca në numrin e lëvizjeve të ligjshme
    # (sa më shumë lëvizje, aq më mirë përgjithësisht).
    mobility_score = len(list(board.legal_moves))
    total_score = material_score + 0.1 * mobility_score
    
    # Kthejmë një numër të plotë. (Rrumbullakojmë nëse është e nevojshme.)
    return int(round(total_score))


def alpha_beta_search(board: chess.Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
    """
    Kryen minimax me prerje alpha-beta:
      - board: tabela aktuale chess.Board
      - depth: thellësia e kërkimit
      - alpha, beta: kufinjtë alpha-beta
      - maximizing_player: True nëse jemi në radhën e “maksimizuesit”, False nëse jemi në radhën e “minimizuesit”

    Kthen një vlerësim numerik të tabelës.
    """
    # 1) Nëse arrijmë thellësinë 0 ose loja ka mbaruar, vlerësojmë
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        # Pa lëvizje të ligjshme => mund të jetë barazim ose mat,
        # por mund të bëjmë vlerësim edhe këtu
        return evaluate_board(board)

    if maximizing_player:
        value = float('-inf')
        for move in legal_moves:
            board.push(move)
            # Pas lëvizjes, radha i kalon kundërshtarit, kështu që “maximizing_player” flip
            value = max(value, alpha_beta_search(board, depth - 1, alpha, beta, False))
            board.pop()  # kthe lëvizjen prapa

            alpha = max(alpha, value)
            if alpha >= beta:
                # Beta cut-off (prerje)
                break
        return value
    else:
        value = float('inf')
        for move in legal_moves:
            board.push(move)
            # Bëhet radha e kundërshtarit => “maximizing_player” flip
            value = min(value, alpha_beta_search(board, depth - 1, alpha, beta, True))
            board.pop()

            beta = min(beta, value)
            if beta <= alpha:
                # Alpha cut-off (prerje)
                break
        return value


def find_best_move(board: chess.Board, depth: int = 3) -> chess.Move:
    """
    Duke pasur një tabelë dhe një kufi thellësie,
    kthen lëvizjen më të mirë sipas minimax me prerjen alpha-beta.
    (Nga perspektiva e board.turn)
    """
    best_move = None
    best_value = float('-inf') if board.turn else float('inf')

    for move in board.legal_moves:
        board.push(move)
        # Vlerësojmë pozicionin pas kësaj lëvizjeje
        value = alpha_beta_search(board, depth - 1, alpha=float('-inf'), beta=float('inf'), maximizing_player=(not board.turn))
        board.pop()

        # Nëse është rradha e bardhës, maximizojmë
        if board.turn:  
            if value > best_value:
                best_value = value
                best_move = move
        else:  # nëse është rradha e zezës, minimizojmë
            if value < best_value:
                best_value = value
                best_move = move

    return best_move


def main():
    # Mund të vendosni një FEN kustom që përfaqëson një pozicion “mid-game”.
    # Më poshtë një shembull i një pozicioni rastësor (s’është domosdoshmërisht i balancuar).
    # (Këtu është radha e bardhës.)
    fen = "r1bq1rk1/pppp1ppp/2n2n2/1Bb1p3/2B5/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 1"
    board = chess.Board(fen)

    print("Tabela fillestare (FEN):")
    print(board)
    print("Radha e tabelës:", "Bardhë" if board.turn else "Zezë")

    search_depth = int(input("Thellësia e kërkimit: "))
    best = find_best_move(board, depth=search_depth)

    print(f"\nLëvizja më e mirë e sugjeruar nga MiniMax me alpha-beta (thellësi={search_depth}):", best)
    if best is not None:
        board.push(best)
        print("Tabela pas lëvizjes më të mirë:")
        print(board)
    else:
        print("S’ka lëvizje të ligjshme ose s’ka lëvizje më të mirë.")

if __name__ == "__main__":
    main()