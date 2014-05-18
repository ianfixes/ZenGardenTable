
from sensor import DisplacementSensor, DisplacementError

DEBUG = False


class BoustrophedonSolver(object):

    def __init__(self, rockpoint_array, canvas, ball_radius):
        self.rockpoint = rockpoint_array
        self.canvas = canvas
        self.radius = ball_radius
        self.sensor = DisplacementSensor(self.radius, DEBUG)

    def solve(self):

       covered = [[False for y in col] for col in self.rockpoint]

       for x, row in enumerate(self.rockpoint):
           print "testing col", x
           if x < (self.radius - 1): continue
           if x > (len(self.rockpoint) - self.radius): continue
           for y, is_rock in enumerate(row):
               #print "testing ", x, y
               # test coverage and verify no displacement
               coverage = self.sensor.ball_coverage(x, y)
               if DEBUG: print "ball coverage is", coverage
               try:
                   d = self.sensor.displacement(x, y, self.is_rockpoint) #, coverage)
                   if (0, 0) == d:
                       # all points ok
                       for xc, yc in coverage:
                           covered[xc][yc] = True
               except DisplacementError:
                   pass
               except IndexError:
                   print "failed", xc, yc
                   raise
               except:
                   raise

       print "Drawing cols",
       for x, row in enumerate(self.rockpoint):
           print ".",
           for y, is_rock in enumerate(row):
               if covered[x][y]:
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
