import random
import chess
import math
import time

class Game():
    def __init__(self):
        self.board = chess.Board()
        self.depth = 3
        self.move_number = 0

        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.15,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0 
        }

        self.play()

    def play(self):
        self.start = time.time()
        while self.board.outcome() is None:
            self.search()
        self.end = time.time()
        self.print_end_stats()

    def print_end_stats(self):
        print("######################################")
        print(self.evaluate())
        print(self.board.result(), self.board.outcome().termination)
        print(f"Time taken: {self.end - self.start}")
    
    def search(self):
        moves = list(self.board.legal_moves)
        move_evals = {}

        maximizingPlayer = self.board.turn == chess.WHITE

        for move in moves:
            self.board.push(move)
            move_evals[move] = self.minimax(self.depth - 1, -math.inf, math.inf, not maximizingPlayer)
            self.board.pop()

        if maximizingPlayer:
            best_move = max(move_evals, key=move_evals.get)
        else:
            best_move = min(move_evals, key=move_evals.get)

        self.move_number = math.floor(self.board.ply() / 2)
        print(f"Move #{self.move_number + 1} - {best_move} | {move_evals[best_move]}")

        return self.board.push(best_move)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = -math.inf
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, not maximizing_player)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, not maximizing_player)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self):                 
        eval = 0
        eval += self.check_is_checkmate()
        eval += self.check_is_check()
        eval += self.check_material_balance()

        return eval + random.uniform(-0.001, 0.001)
    
    def check_is_checkmate(self):
        if self.board.is_checkmate():
            if self.board.turn == chess.WHITE:
                return -100
            else:
                return 100
        else:
            return 0

    def check_material_balance(self):
        eval = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = self.piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    eval += value
                else:
                    eval -= value
        return eval

    def check_is_check(self):
        if self.board.is_check():
            if self.board.turn == chess.WHITE:
                return -2
            else:
                return 2
        return 0


if __name__ == "__main__":
    game = Game()