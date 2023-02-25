# copyright: Yongjian Feng
from GameBoardReal import GameBoardReal
from Data import Data


class GameBoard:

    def __init__(self):
        self.win_w = 800
        self.win_h = 600

        self.bg_color = (255, 255, 255)
        self.fps = 60

        self.title = 'Powered by GameBoard'

        self.updater = None
        self.data = None

        self.gb = GameBoardReal(self)

    def init(self):
        # separate this from __init__ so caller can
        # have a change to change the params
        self.data = Data(self.win_w, self.win_h)
        self.gb.init()

    def start(self):
        self.gb.start()

    def set_flying(self):
        self.gb.set_flying()

    def set_expose(self):
        self.gb.set_expose()


if __name__ == '__main__':
    gb = GameBoard()
    gb.init()
    gb.start()

