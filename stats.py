

class Stats():
    def __init__(self, stngs):
        self.stngs = stngs
        self.reset_stats()

    def reset_stats(self):
        self.life = self.stngs.max_lifes
        self.score = 0
        self.state = 1