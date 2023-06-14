import sys, os, traceback, colorama, random, chess, chess.engine, copy
from rich import print

print(os.getcwd(), sys.version)


class Square:
    def __init__(self, color):
        self.color = color
        self.cord = cord


class Chessboard:
    def __init__(self):
        try:
            self.X = ["A", "B", "C", "D", "E", "F", "G", "H"]
            self.Y = ["1", "2", "3", "4", "5", "6", "7", "8"]
            self.squares = sorted(
                [(X + Y) for X in self.X for Y in self.Y[::-1]],
                key=lambda x: x[1],
                reverse=True,
            )

            self.colors = {
                S: "DARK"
                if (int(S[1]) + (1 + int(self.Y[self.X.index(S[0])]))) % 2
                else "LIGHT"
                for S in self.squares
            }
            self.RULE = "This is the rule : X+Y % 2 == DARK"

            # INIT STOCKFISH:
            board = chess.Board()
            stockfish_path = (
                "D:\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe"
            )
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

        except Exception as e:
            print(e, traceback.print_stack())
            print(repr(traceback.format_stack()))

    def __str__(self):
        return str(self.squares)

    def show_board(self):
        colorama.init(autoreset=False)
        idx = 0
        for horizontal in self.squares:
            if self.colors[horizontal] == "DARK":
                print(colorama.Fore.CYAN, end="", sep="")
            print(f"[ {horizontal} ]", end="", sep="")
            print(colorama.Style.RESET_ALL, end="", sep="")
            idx += 1
            if idx == 8:
                print("\n")
                idx = 0

    def colors(self):
        return self.colors

    def train_squares(self, rounds: int):
        """
        This is a simple blind chess trainer,
        given the number of rounds, it will ask
        about the color of a random square.
        """
        pts = 0
        for r in range(rounds):
            print("ROUND #", r)
            square = random.choice(self.squares)
            answer = self.colors[square]
            guess = input("Tell me is it light or a dark square: " + square + "\n")
            if guess.lower() == answer.lower():
                print("Correct. Point for you.")
                pts += 1
            else:
                print("Wrong. Try harder.", square, answer, self.RULE)
        print("End. Your score is", pts)

    def train_knight(self, rounds):
        pts, ptsmax = 0, 0

        def permutate(X: str, Y: str):
            moves = []
            c1, c2 = [-2, 2], [-1, 1]
            for cord1 in c1:
                for cord2 in c2:
                    X2 = self.X.index(X) + cord1
                    Y1 = self.Y.index(Y) + cord2
                    # print("X2:", X2, "Y1:", Y1) # DEBUG
                    if 0 < X2 < 8 and 0 < Y1 < 8:
                        moves.append(self.X[X2] + self.Y[Y1])
                    X1 = self.X.index(X) + cord2
                    Y2 = self.Y.index(Y) + cord1
                    # print("X1:", X1, "Y2:", Y2) # DEBUG
                    if 0 < X1 < 8 and 0 < Y2 < 8:
                        moves.append(self.X[X1] + self.Y[Y2])

            return moves

        for r in range(rounds):
            r += 1
            print("ROUND #", r)
            square = random.choice(self.squares)
            col = self.colors[square]
            X, Y = list(square)

            moves = permutate(X, Y)
            ptsmax += len(moves)
            answer = input(
                f"Tell me the possible knight moves for square {square}, separated by a space.\n"
            ).replace(",", " ")
            answer = [x.upper() for x in answer.split() if x]
            for a in answer:
                if a.upper() in moves:
                    pts += 1
                    print("Correct answer. Point for you.")
                else:
                    print(f"Wrong answer {a}. Try harder.")
            missed = [m for m in moves if m not in answer]
            if missed:
                print(f"Missed {len(missed)} moves were:", moves)
        print(f"The end. Your score is {pts} / {ptsmax} - {pts*100/ptsmax:.2F}%")


B = Chessboard()
print(B.show_board())
print(B.colors)
# print(B.train_squares(4))
print(B.train_knight(2))
