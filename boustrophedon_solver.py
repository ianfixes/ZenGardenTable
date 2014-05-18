
from sensor import DisplacementSensor, DisplacementError

DEBUG = False


class BoustrophedonSolver(object):

    def __init__(self, rockpoint_array, canvas, ball_radius):
        self.rockpoint = rockpoint_array
        self.canvas = canvas
        self.radius = ball_radius
        self.sensor = DisplacementSensor(self.radius, DEBUG)
        self.covered = None


    def reset(self):
        self.covered_first_point = False
        self.covered = [[False for y in col] for col in self.rockpoint]


    def visit_point(self, x, y):
        try:
            d = self.sensor.displacement(x, y, self.is_rockpoint) #, coverage)
            if (0, 0) == d:
                # all points ok
                if self.covered_first_point:
                    coverage = self.sensor.ball_shell(x, y)
                else:
                    self.covered_first_point = True
                    coverage = self.sensor.ball_coverage(x, y)

                for xc, yc in coverage:
                    self.covered[xc][yc] = True
        except DisplacementError:
            pass
        except IndexError:
            print "failed", xc, yc
            raise
        except:
            raise


    # use fake omnipotent algorithm to exercise coverage algorithm
    def cover_bogo(self):
        for x, row in enumerate(self.rockpoint):
            print "testing col", x
            if x < (self.radius - 1): continue
            if x > (len(self.rockpoint) - self.radius): continue
            for y, is_rock in enumerate(row):
                if y < (self.radius - 1): continue
                if y > (len(self.rockpoint) - self.radius): continue
                #print "testing ", x, y
                # test coverage and verify no displacement
                self.visit_point(x, y)



    def solve(self):
        self.reset()

        self.cover_bogo()

        print "Drawing cols",
        for x, row in enumerate(self.rockpoint):
            print ".",
            for y, is_rock in enumerate(row):
                if self.covered[x][y]:
                    self.draw_point(x, y, "yellow")

        print



    def is_rockpoint(self, x, y):
        if 0 > x or 0 > y: return True
        if x >= len(self.rockpoint): return True

        col = self.rockpoint[x]
        if y >= len(col): return True
        return col[y]


    def draw_point(self, x, y, color="black"):
        self.canvas.create_line(x, y, x+1, y, smooth=False, fill=color)


    def animate(self):
        self.animation_steps = 100
        self.draw_frame()
        print "Animate is done"


    def draw_frame(self):
        if 0 >= self.animation_steps:
            print "DONE"
        else:
            p  = self.animation_steps
            np = p - 1

            self.canvas.create_line(p, p, np, np, smooth=False, fill="blue")
            self.animation_steps = np

            #self.update_idletasks()

            self.canvas.after(100, self.draw_frame)
