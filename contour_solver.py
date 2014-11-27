
from sensor import ProximitySensor
from ball import Ball
import sys

DEBUG = False


class ContourSolver(object):

    def __init__(self, table, ball, is_rockpoint):
        self.table = table
        self.ball = ball
        self.canvas = table.drawing_area
        self.contours = []
        self.is_rockpoint = is_rockpoint


    def solve(self, visited, num_contours):
        max_prox = (self.ball.radius * num_contours) + 1
        proxball = Ball(max_prox)
        ps = ProximitySensor(proxball, False)
        ps.set_rockpoint_fn(self.is_rockpoint)
        
        visited_hash = dict([(x, True) for x in visited])
        
        fudge = 0.71

        sys.stdout.write("generating proximity map")
        hundredth = int(len(visited) / 100)
        for i, (x, y) in enumerate(visited):
            if 0 == i % hundredth:
                sys.stdout.write(".")
                sys.stdout.flush()
            prox = ps.proximity(x, y, visited_hash)
            if prox is None: continue


            if 1 <= (prox % self.ball.radius) <= (1 + fudge):
                color = "black"
            else:
                norm_prox = min(128, int(prox / max_prox * 128))
                color = "#00%02X%02X" % (127 + norm_prox, 255 - norm_prox)

            self.table.draw_point(x, y, color)
        print
            


    def draw_contours(self):
        for c in self.contours:
            for (x, y) in c:
                self.table.draw_point(x, y, "blue")
