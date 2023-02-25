# copyright: Yongjian Feng

class Data:

    BLACK   = (0,   0,  0)
    BLUE    = (0,   0,  255)

    def __init__(self, w, h):
        self.n_x = 0
        self.n_y = 0
        self.v_x = 0
        self.v_y = 0

        self.vir_x = -1
        self.vir_y = 0

        # radius
        self.vir_r = 20

        # game boad data
        self.w = w
        self.h = h

        # other data
        self.ground_y = 0

        self.launched = False

        self.resize()

    def set_npos(self, x, y):
        self.n_x = x
        self.n_y = y

    def set_vpos(self, x):
        self.vir_x = x

    def set_vsize(self, r):
        self.vir_r = r

    def set_speed(self, v_x, v_y):
        self.v_x = v_x
        self.v_y = v_y

    def resize(self):
        self.ground_y = 0.8*self.h
        self.vir_y = self.ground_y
