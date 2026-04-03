import numpy as np
import sys
from othello import Board

board = Board()

class Game:
    def __init__(self):
        self.white_count = 2
        self.black_count = 2
        self.blank_count = 60

    def input_stone(self):
        print("石を置く場所を1~8で入力してください。パス：(9, 9)、終了：(0, 0)")
        print("xが縦、yが横の座標です。")
        print("左上が(1, 1)、右下が(8, 8)です。")
        x = int(input("x >> "))
        y = int(input("y >> "))
        
        try:
            x -= 1
            y -= 1
        except:
            self.input_stone()
        return x, y
    
    def pass_turn(self):
        board.pass_count += 1
        board.turnchange()
        if board.pass_count == 2:
            self.gameset()
        return True
    
    def gameset(self):
        print("ゲーム終了")
        self.count_sys()
        print("白の石：", self.white_count)
        print("黒の石：", self.black_count)
        if self.white_count > self.black_count:
            print("白の勝ちです")
        elif self.white_count < self.black_count:
            print("黒の勝ちです")
        elif self.white_count == self.black_count:
            print("引き分けです")
        sys.exit()

    def count_sys(self):
        self.white_count = np.sum(board.cell == board.WHITE)
        self.black_count = np.sum(board.cell == board.BLACK)
        self.blank_count = np.sum(board.cell == board.BLANK)

    def one_turn(self):
        if board.check_put_place(board.current):
            (x, y) = self.input_stone()
            board.put_stone(x, y, board.current)
            if not board.put_stone(x, y, board.current):
                if (x, y) == (8, 8):
                    self.pass_turn()
                elif (x, y) == (-1, -1):
                    self.gameset()
        else:
            self.pass_turn()

    def gameplay(self):
        while self.blank_count > 0:
            board.display()
            print('---'*10)
            print("ターン：", board.turn, end=" ")
            if board.current == -1:
                print(", 黒のターン")
            elif board.current == 1:
                print(", 白のターン")
            board.turn += 1
            self.one_turn()
        self.gameset()