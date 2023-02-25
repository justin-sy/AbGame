# Copyright: Justin Feng
from GameBoard import GameBoard
import random


class AbGame:

    def __init__(self):
        self.gb = GameBoard()
        self.acc = 0.00125
        self.pre_vy = 0
        self.init_vy = False
        # self.init = False

    def run(self):
        self.gb.updater = self
        self.gb.init()
        self.gb.start()

    #
    # This is the method being called for each iteration to update the location of the flying
    # needle.
    def update(self, data):

        if data.vir_x <= 0:
          return
        if self.init_vy == False and data.v_y > 0:
          self.pre_vy = data.v_y
          self.init_vy = True

        if data.launched:
          self.pre_vy = data.v_y
          data.launched = False

        # if self.init:
        #   self.pre_vy = data.v_y
        # if data.n_y > 540:
        #   self.init = True
        #   data.n_x = -40
        #   return
        # else:
        #   self.init = False
        
        
        data.n_x += data.v_x
        self.pre_vy -= self.acc
        data.n_y -= self.pre_vy
        return

    # This is the method to start up a new game. You need to set the location of the virus
    def start_new_game(self):

        self.gb.data.vir_x = random.randint(0,800)
        return



if __name__ == '__main__':
    abgame = AbGame()
    abgame.run()
