

class Background(object):

    def __init__(self, table, ball):
        self.table = table
        self.ball = ball
        self.canvas = table.drawing_area


class LinearBackground(Background):

    def __init__(self, table, ball):
        super(LinearBackground, self).__init__(table, ball)
        self.lines = []

    def solve(self, visited, is_foreground):
        diameter = self.ball.radius * 2
        bins = int(self.table.table_height / diameter)
        self.lines = [[]] * bins
        for (x, y) in visited:
            if is_foreground[(x, y)]: continue
            if 0 == y % diameter:
                bin = int(y / diameter)
                self.lines[bin].append((x, y))
        
    def draw(self):
        for i, l in enumerate(self.lines):
            for (x, y) in l:
                self.table.draw_point(x, y, "black")
