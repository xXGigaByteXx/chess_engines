import chess
import threading
import ctypes

board = chess.Board()
COLOR = "WHITE"


def minimax(position, depth, max_player):
    if depth == 0 or winner(position) is not None:
        return evaluate(position), position.peek()

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for board_pos, move in get_all_moves(position):
            evaluation = minimax(board_pos, depth-1, False)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for board_pos, move in get_all_moves(position):
            evaluation = minimax(board_pos, depth-1, True)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move


def get_all_moves(board_pos):
    moves = []

    for move in board_pos.generate_legal_moves():
        temp_board_pos = chess.Board(board_pos.fen())
        temp_board_pos.push(move)
        moves.append((temp_board_pos, move))

    return moves


def evaluate(position):
    pieces = position.fen().split(" ")[0]
    curr_eval = 0
    curr_eval += (pieces.count("P") - pieces.count("p"))
    curr_eval += 3 * (pieces.count("N") + pieces.count("B") - pieces.count("n") - pieces.count("b"))
    curr_eval += 5 * (pieces.count("R") - pieces.count("r"))
    curr_eval += 9 * (pieces.count("Q") - pieces.count("q"))
    return curr_eval


def winner(position):
    result = position.result()
    if result == "*":
        return None
    elif result == "1-0":
        return "WHITE"
    else:
        return "BLACK"


def print_best(position, max_depth, color):
    best_move = minimax(position, max_depth, True if color.strip().lower() in ("white", "w") else False)[1]

    print(f"bestmove {best_move}")


def Quit():  # Function to crash the interpreter and terminate all threads.
    ctypes.pointer(ctypes.c_char.from_address(5))[0]


def start():
    while True:
        msg = input().lower().strip()
        if msg == "quit":
            Quit()
        elif msg == "isready":
            print("readyok")
        elif msg == "uci":
            print("uciok")
        elif msg == "d":
            print(board)
        elif msg == "ucinewgme":
            board.reset()

        elif msg.startswith("position"):
            msg = msg.replace("position", "").strip()
            if msg.startswith("startpos"):
                if "moves" in msg:
                    board.reset()
                    for m in msg.replace("startpos moves", "").strip().split(" "):
                        board.push_uci(m)
                else:
                    board.reset()

            elif msg.startswith("fen"):
                board.set_fen(msg.replace("fen", "").strip())

        elif msg.startswith("go") or msg.startswith("CABALTICA"):
            print_best(board, 3, COLOR)

        else:
            print(f"Unknown command: {msg}")


start()
