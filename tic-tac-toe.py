import random
import numpy


class Player:
    def __init__(self, mark: str) -> None:
        self.human = None
        self.random = None
        self.master = None
        self.mark = mark
        self.opponent = "X" if self.mark == "O" else "O"
        self.choose_controller()

    def return_mark(self):
        return self.mark

    def choose_controller(self):
        response = input("Please decide who controlls this player - (H)uman, (C)omputer or (M)aster : ").upper()
        while response not in ["H", "C", "M"]:
            response = input("Please respond with H, C or M : ").upper()
        if response == "H":
            self.human = True
        elif response == "C":
            self.random = True
        elif response == "M":
            self.master = True
        else:
            exit("Something went wrong...")

    def make_turn(self, board: numpy.ndarray):
        if self.human:
            return self.make_human_turn(board)
        elif self.random:
            return self.make_random_turn(board)
        elif self.master:
            return self.make_master_turn(board)

    def make_human_turn(self, board: numpy.ndarray):
        def get_digit():
            choice = input("Please choose a cell to mark [1-9] : ")
            while not choice.isdigit() or int(choice) < 1 or int(choice) > 9:
                choice = input("Please use digits [1-9] : ")
            return int(choice)
        
        flat_board = board.ravel()
        while True:
            c = get_digit() - 1
            if flat_board[c] == 0:
                return (c, self.return_mark())
            else:
                print("This cell is unavailable.")

    def make_random_turn(self, board: numpy.ndarray):
        board = board.ravel()
        possible_cells = []
        for pos, mark in enumerate(board):
            if mark == 0:
                possible_cells.append(pos)
        choice = random.choice(possible_cells)
        print(f"Computer '{self.mark}' marks a cell.")
        return (choice, self.return_mark())

    def make_master_turn(self, board: numpy.ndarray):

        def minmaxer(_board: numpy.ndarray, my_turn=True):
            """Определяет, какая из доступных клеток самая выгодная. Должен вернуть оценку этой клетки и ее номер."""
            possible_cells = []
            for pos, fill in enumerate(_board.ravel().tolist()):
                if fill == 0:
                    possible_cells.append([0, pos + 1]) # 0 - score, pos - cell position

            for cell in range(len(possible_cells)):
                new_board = _board.copy()
                new_board[(possible_cells[cell][1] - 1) // 3, (possible_cells[cell][1] - 1) % 3] = self.mark if my_turn == True else self.opponent
                result = Game.check_board(new_board)
                if result != 0 and result is not None:
                    score = len(possible_cells) * (-1 if my_turn == False else 1)
                    possible_cells[cell][0] = score
                elif result == 0:
                    possible_cells[cell][0] = 0
                else:
                    possible_cells[cell][0] = minmaxer(new_board, my_turn=(False if my_turn == True else True))[0]

            best_cells = []
            for cell in possible_cells:
                if cell[0] == max(possible_cells)[0]:
                    best_cells.append(cell)
            best_option = random.choice(best_cells)

            return best_option

        return (minmaxer(board)[1], self.return_mark())


class Game:
    def __init__(self) -> None:
        print("\n\nHello! This is Tic-Tac-Toe game. First, choose who controls players.")
        self.board = numpy.zeros((3, 3), dtype='O')
        self.player1 = None
        self.player2 = None
        self.player1_score = 0
        self.player2_score = 0
        self.add_players()
        self.game_cycle()

    def add_players(self):
        print("\nPlayer one:")
        self.player1 = Player("X")
        print("\nPlayer two:")
        self.player2 = Player("O")

    def draw_board(self):
        print("\n")
        print(f" {' ' if self.board[0, 0] == 0 else self.board[0, 0]} | {' ' if self.board[0, 1] == 0 else self.board[0, 1]} | {' ' if self.board[0, 2] == 0 else self.board[0, 2]} ")
        print(f"---|---|---")
        print(f" {' ' if self.board[1, 0] == 0 else self.board[1, 0]} | {' ' if self.board[1, 1] == 0 else self.board[1, 1]} | {' ' if self.board[1, 2] == 0 else self.board[1, 2]} ")
        print(f"---|---|---")
        print(f" {' ' if self.board[2, 0] == 0 else self.board[2, 0]} | {' ' if self.board[2, 1] == 0 else self.board[2, 1]} | {' ' if self.board[2, 2] == 0 else self.board[2, 2]} ")
        
    def check_board(board):
        rows_cols_diags = board.tolist() + board.transpose().tolist() + [board.diagonal().tolist()] + [numpy.fliplr(board).diagonal().tolist()]

        for line in rows_cols_diags:
            if len(set(line)) == 1 and set(line).pop() != 0:
                return set(line).pop()
        
        if 0 not in board.ravel().tolist():
            return 0

        return None

    def game_cycle(self):
        print("\nGame start!")
        player_one_move = True
        while True:
            while player_one_move is True:
                self.draw_board()
                print(f"Player {self.player1.return_mark()}:")
                cell, mark = self.player1.make_turn(self.board)
                self.board[cell // 3, cell % 3] = mark
                player_one_move = False

            if Game.check_board(self.board) is not None:
                return self.game_end(Game.check_board(self.board))

            while player_one_move is False:
                self.draw_board()
                print(f"Player {self.player2.return_mark()}:")
                cell, mark = self.player2.make_turn(self.board)
                self.board[cell // 3, cell % 3] = mark
                player_one_move = True

            if Game.check_board(self.board) is not None:
                return self.game_end(Game.check_board(self.board))

    def game_end(self, result):
        self.draw_board()

        if result == 0:
            print("It's a tie!")
        elif result == self.player1.return_mark():
            print("Player 1 wins!")
            self.player1_score += 1
        elif result == self.player2.return_mark():
            print("Player 2 wins!")
            self.player2_score += 1
        else:
            print("Something went wrong!")

            
        print(f"Score: Player 1 - {str(self.player1_score)} wins, Player 2 - {str(self.player2_score)} wins.\n")

        if input("If you want to quit the game, type N : ").upper() == "N":
            exit("\nGoodbye!\n")
        else:
            self.board = numpy.zeros((3, 3), dtype='O')
            self.game_cycle()

        
if __name__ == "__main__":
    Game()
