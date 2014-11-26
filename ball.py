
import math

class Ball(object):

    def __init__(self, radius):
        self.radius = radius
        self.coverage_template = Ball.get_coverage_template(radius)
        self.shell_template    = Ball.get_shell_template(self.coverage_template)


    @staticmethod
    def get_coverage_template(radius):
        """
        get a list of (x, y) points covered by a ball with radius
        
        """

        rr = radius - 1
        
        out = []
        for x in range(0 - rr, rr + 1):
            for y in range(0 - rr, rr + 1):
                if rr >= math.hypot(x, y):
                    out.append((x,y))
        return out


    @staticmethod
    def get_shell_template(template):
        """
        get a list of (x, y) points that touch non-ball neighbors
        
        in other words, any point that has a neighbor that's not in the ball template
        """

        return [(x, y) for (x, y) in template
                if not all(map(template.__contains__,
                               [(x + 1, y),
                                (x - 1, y),
                                (x,     y + 1),
                                (x,     y - 1)]))]


    def coverage(self, ctr_x, ctr_y):
        """
        get a list of (x, y) points covered by a ball at given center (ctr_x, ctr_y)
        
        points that overlap the edges are considered
        """
        
        return [(x + ctr_x, y + ctr_y) for (x, y) in self.coverage_template]



    def shell(self, ctr_x, ctr_y):
        """
        get a list of (x, y) points covered by the shell of a ball at given center
        """
        
        return [(x + ctr_x, y + ctr_y) for (x, y) in self.shell_template]


