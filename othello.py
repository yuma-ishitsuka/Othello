import numpy as np

class Board:
    # 初期設定
    def __init__(self):
        self.WHITE = 1
        self.BLACK = -1
        self.BLANK = 0
        self.BOARD_SIZE = 8
        self.DIRECTION_LIST = [-1, 0, 1]
        self.cell = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
        self.cell = self.cell.astype(int)
        self.cell[3][3] = self.cell[4][4] = 1
        self.cell[3][4] = self.cell[4][3] = -1
        self.current = self.BLACK
        self.pass_count = 0
        self.turn = 1

    # ターンチェンジ
    def turn_change(self):
        self.current *= -1
    
    # その座標が範囲内かチェック
    def range_check(self, x, y):
        if x == None: x = -1
        if y == None: y = -1
        if x < 0 or self.BOARD_SIZE <= x or y < 0 or self.BOARD_SIZE <= y:
            return False
        return True
    
    # その場所に置けるかどうかチェック
    def check_can_put(self, x, y, current):
        if not self.range_check(x, y):
            return False
        if not self.cell[x][y] == self.BLANK:
            return False
        elif not self.can_reverse_stone(x, y, current):
            return False
        else: return True

    # (dx, dy)方向にひっくり返せる石があるかどうか
    def can_reverse(self, dx, dy, x, y, current):
        if not self.range_check(x+dx, y+dy):
            return False
        length = 0
        while self.cell[x+dx][y+dy] == -current:
            x += dx
            y += dy
            length += 1
            if not self.range_check(x+dx, y+dy):
                return False
            if self.cell[x+dx][y+dy] == current:
                return length
        else:
            return False

    def can_reverse_stone(self, x, y, current):
        for dy in self.DIRECTION_LIST:
            for dx in self.DIRECTION_LIST:
                if dx == dy == 0:
                    continue
                elif not self.range_check(x+dx, y+dy):
                    continue
                elif not self.can_reverse(dx, dy, x, y, current):
                    continue
                else: return True

    def reverse_stone(self, x, y, current):
        for dy in self.DIRECTION_LIST:
            for dx in self.DIRECTION_LIST:
                length = self.can_reverse(dx, dy, x, y, current)
                if length == False:
                    length = 0
                if length > 0:
                    for j in range(length):
                        k = j + 1
                        self.cell[x+k*dx][y+k*dy] *= -1
    
    def display(self):
        print("---"*10)
        print("\n", end=" ")
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.cell[x][y] == self.WHITE:
                    print("W", end=" ")
                elif self.cell[x][y] == self.BLACK:
                    print("B", end=" ")
                else:
                    print("*", end=" ")
            print("\n", end=" ")
        print("\n", end=" ")

    def put_stone(self, x, y, current):
        self.pass_count = 0
        self.cell[x][y] = current
        self.reverse_stone(x, y, current)
        self.turn_change()
        
        
    def check_put_place(self, current):
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if self.check_can_put(x, y, current):
                    return True
                else:
                    continue
        return False