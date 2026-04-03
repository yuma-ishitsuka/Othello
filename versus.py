from game import Game
from othello import Board
import numpy as np
import random
import sys
import time

board = Board()
game = Game()

class Versus:
    def __init__(self):
        self.pl_current = board.BLACK
        self.cpu_current = board.WHITE

        self.black_count = 2
        self.white_count = 2
        self.blank_count = 60

        self.priority = [[9,4,5,5,5,5,4,9],
                         [4,1,3,3,3,3,1,4],
                         [5,3,4,4,4,4,3,5],
                         [5,3,4,4,4,4,3,5],
                         [5,3,4,4,4,4,3,5],
                         [5,3,4,4,4,4,3,5],
                         [4,1,3,3,3,3,1,4],
                         [9,4,5,5,5,5,4,9]]

    def search_can_place(self):
        can_put_place = np.zeros((board.BOARD_SIZE, board.BOARD_SIZE))
        for x in range(board.BOARD_SIZE):
            for y in range(board.BOARD_SIZE):
                if board.check_can_put(x, y, self.cpu_current):
                    can_put_place[x][y] = 1
            
        return can_put_place
    
    def search_place(self):
        can_list = []
        can_put = self.search_can_place()
        # print(can_put)
        for x in range(board.BOARD_SIZE):
            for y in range(board.BOARD_SIZE):
                if can_put[x][y] == 1:
                    can_put[x][y] = self.priority[x][y]
                else:
                    can_put[x][y] = 0
        # print(can_put)
        for x in range(board.BOARD_SIZE):
            for y in range(board.BOARD_SIZE):
                if can_put[x][y] == np.max(can_put):
                    can_list.append((x, y))
        
        if len(can_list) > 0:
            point = random.choice(can_list)
            return point
        elif any(self.cpu_current in row for row in board.cell):
            return (8, 8)
        else:
            return (-1, -1)
    
    def player_turn(self, first):
        if first == 1:
            self.pl_current = board.WHITE
            self.cpu_current = board.BLACK
        elif first == 0:
            self.pl_current = board.BLACK
            self.cpu_current = board.WHITE

    def pass_turn_vs(self):
        board.pass_count += 1
        if board.pass_count == 2:
            self.versus_set()
        return True
        
    def put_stone_vs(self, x, y, current):
        if board.check_can_put(x, y, current):
            board.pass_count = 0
            board.cell[x][y] = current
            board.reverse_stone(x, y, current)
            return True
        else:
            return False
    
    def cpu_turn(self, current):
        if board.check_put_place(current):
            x, y = self.search_place()
            # print((x, y))
            self.put_stone_vs(x, y, current)
            if self.put_stone_vs(x, y, current):
                print(f"{(x+1, y+1)}に石を置きました。")
            elif not self.put_stone_vs(x, y, current):
                if (x, y) == (8, 8):
                    print("CPUはパスしました。")
                    self.pass_turn_vs()
                elif (x, y) == (-1, -1):
                    print("CPUは降参しました。")
                    self.versus_set()
                else:
                    print(f"{(x+1, y+1)}に置けませんでした。置き直します。")
                    self.cpu_turn(current)
        else:
            print("CPUはパスしました。")
            self.pass_turn_vs()

    def pl_turn(self, current):
        if board.check_put_place(current):
            (x, y) = game.input_stone()
            self.put_stone_vs(x, y, current)
            if self.put_stone_vs(x, y, current):
                print(f"{(x+1, y+1)}に石を置きました。")
            elif not self.put_stone_vs(x, y, current):
                if (x, y) == (8, 8):
                    print("パスしました。")
                    self.pass_turn_vs()
                elif (x, y) == (-1, -1):
                    print("降参しました。")
                    self.versus_set()
                else:
                    print(f"{(x+1, y+1)}に置けませんでした。置き直してください。")
                    self.pl_turn(current)
        else:
            print("パスしました。")
            self.pass_turn_vs()

    def one_cycle(self, first):
        if first == 1:
            print("CPUのターンです。")
            print("CPU思考中...")
            time.sleep(2)
            self.cpu_turn(self.cpu_current)
            board.display()
            print("あなたのターンです。")
            self.pl_turn(self.pl_current)
            board.display()

        elif first == 0:
            print("あなたのターンです。")
            self.pl_turn(self.pl_current)
            board.display()
            print("CPUのターンです。")
            print("CPU思考中...")
            time.sleep(2)
            self.cpu_turn(self.cpu_current)
            board.display()

    def count(self):
        self.black_count = np.sum(board.cell==board.BLACK)
        self.white_count = np.sum(board.cell==board.WHITE)
        self.blank_count = np.sum(board.cell==board.BLANK)

    def versus_set(self):
        print("ゲーム終了")
        self.count()
        print("白の石：", self.white_count)
        print("黒の石：", self.black_count)
        if self.white_count > self.black_count:
            print("白の勝ちです")
        elif self.white_count < self.black_count:
            print("黒の勝ちです")
        elif self.white_count == self.black_count:
            print("引き分けです")
        sys.exit()

    def versus(self):
        first = int(input("先攻なら0、後攻なら1を入力してください。"))
        if not (first == 0 or first == 1):
            print("もう一度入力してください。")
            self.versus()
        self.player_turn(first)
        board.display()
        while self.blank_count > 0 or self.black_count != 0 or self.white_count != 0:
            self.count()
            if self.black_count == 0 or self.white_count == 0:
                self.versus_set()
            elif self.blank_count == 0:
                self.versus_set()
            else:
                print('---'*10)
                self.one_cycle(first)