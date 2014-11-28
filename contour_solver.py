
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
        self.proximity_map = {}

    def solve(self, visited, num_contours):
        # initialize the proximity sensor
        max_prox = (self.ball.radius * 2 * num_contours) + 1
        proxball = Ball(max_prox)
        ps = ProximitySensor(proxball, False)
        ps.set_rockpoint_fn(self.is_rockpoint)
        visited_hash = dict([(x, True) for x in visited]) # whitelist for prox sensor
        self.proximity_map = {}
        
        fudge = 0.71 # 1 / sqrt(2)

        # collect all contour points
        all_contour_points = []
        for i, (x, y) in enumerate(visited):
            prox = ps.proximity(x, y, visited_hash)
            self.proximity_map[(x, y)] = prox
            if prox is None: continue

            if 1 <= (prox % (self.ball.radius * 2)) <= (1 + fudge):
                color = "black"
                all_contour_points.append((x, y))
            else:
                norm_prox = min(128, int(prox / max_prox * 128))
                color = "#00%02X%02X" % (127 + norm_prox, 255 - norm_prox)

            #self.table.draw_point(x, y, color)

        self.contours = self.get_contiguous_contours(all_contour_points)

        
            
    def get_contiguous_contours(self, all_points):
        print "looking for contiguous contours in", len(all_points), "points"
        contour_point_visited = dict([(p, False) for p in all_points])
        all_contours = []

        def get_first_free_point():
            for (p, v) in contour_point_visited.iteritems():
                if not v: return p
            return None

        def get_neighbors(p):
            (x0, y0) = p
            neighbors = [
                (x0 + 1, y0),
                (x0 - 1, y0),
                (x0,     y0 + 1),
                (x0,     y0 - 1),
                (x0 + 1, y0 + 1),
                (x0 + 1, y0 - 1),
                (x0 - 1, y0 + 1),
                (x0 - 1, y0 - 1),
                ]
            return [n for n in neighbors if n in contour_point_visited and not contour_point_visited[n]]

        while True:
            # pick first contour point in the list, explore its neighbors
            p = get_first_free_point()
            if p is None: break

            contour_point_visited[p] = True
            this_contour = [p]
            to_visit = get_neighbors(p)

            # when there are no more neighbors, add that list to all_contours
            while 0 < len(to_visit):
                p = to_visit.pop()
                contour_point_visited[p] = True
                this_contour.append(p)
                new_neighbors = get_neighbors(p)
                if new_neighbors is not None:
                    to_visit += new_neighbors

            all_contours.append(this_contour)

        return all_contours
            
            

    def draw_contours(self):
        for i, c in enumerate(self.contours):
            for (x, y) in c:
                self.table.draw_point(x, y, "black")
