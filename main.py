from othello import Board
from game import Game
from versus import Versus

def modechange():
    mode = int(input("一人遊びは1、CPU対戦は2を入力してください。>> :"))
    if mode == 1:
        game.gameplay()
    elif mode == 2:
        versus.versus()
    else:
        print("入力が正しくありません。もう一度入力してください。")
        modechange()


if __name__ == "__main__":
    board = Board()
    game = Game()
    versus = Versus()
    modechange()
