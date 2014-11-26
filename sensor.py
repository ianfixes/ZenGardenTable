
import math
import ball

pythag = lambda x1, y1, x2, y2: math.hypot(x1 - x2, y1 - y2)

class DisplacementError(Exception):
    pass


class DisplacementSensor:
    
    def __init__(self, ball, do_debug):
        self.ball = ball
        self.DEBUG = do_debug

    def set_debug(self, enabled):
        self.DEBUG = enabled

    def displacement(self, ctr_x, ctr_y, is_rockpoint_fn):
        """
        calculate the displacement of the ball from its desired center

        for every rock point, draw a radius around them of un-allowable area
        of the remaining points, the one closest to the original center is the displacement
        """

        # find any rock points within the ball
        rockpoints = []
        for point in self.ball.coverage(ctr_x, ctr_y):
            if is_rockpoint_fn(point):
                rockpoints.append(point)

        # early exit if no rocks
        if 0 == len(rockpoints):
            return 0, 0

        if self.DEBUG: print "rockpoints are", rockpoints

        # find the coverage of the rock points, subtract from initial coverage
        uncoverage = set([])
        for (x, y) in rockpoints:
            for (rx, ry) in self.ball.coverage(x, y):
                uncoverage.add((rx, ry))

        # get the squares where coverage is allowed + their distance from ctr
        allowed_coverage = []
        for (x, y) in self.ball.coverage(ctr_x, ctr_y):
            if not (x, y) in uncoverage:
                allowed_coverage.append((x, y, pythag(ctr_x, ctr_y, x, y)))

        # minimum displacement from center
        # favor the lower x, y
        def my_min(ac1, ac2):
            if ac1 is None:
                return ac2
            elif ac2 is None:
                return ac1

            x1, y1, d1 = ac1
            x2, y2, d2 = ac2

            if d1 > d2:
                return ac2
            elif d1 < d2:
                return ac1
            else:
                if x1 == x2:
                    if y1 < y2:
                        return ac1
                    else:
                        return ac2
                elif x1 > x2:
                    return ac2
                else:
                    return ac1

        # find what remaining point is the minimum distance from the center
        # start with a bogus point
        min_distance_point = None
        for pt in allowed_coverage:
            min_distance_point = my_min(min_distance_point, pt)

        if min_distance_point is None:
            raise DisplacementError("No allowed coverage for %d, %d" % (ctr_x, ctr_y))

        xm, ym, _ = min_distance_point
        return xm - ctr_x, ym - ctr_y



