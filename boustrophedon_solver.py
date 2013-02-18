
import math

class BoustrophedonSolver(object):
   def __init__(self, rockpoint_array, canvas, ball_radius):
      self.rockpoint = rockpoint_array
      self.canvas = canvas
      self.radius = ball_radius

   def solve(self):
       self.draw_point(599, 599, "blue")

       self.draw_point(0,0)

       ctr = 2
       for r in range(1, 2):
           self.radius = r
           covered = self.ball_coverage(ctr, ctr)
           print "points with radius", r, covered
           for (x, y) in covered:
               print "drawing", x, y
               self.draw_point(x, y, "blue")
           ctr = ctr + (r * 2)
       

   def ball_coverage(self, ctr_x, ctr_y):
       """
       get a list of (x, y) points covered by a ball at given center (ctr_x, ctr_y)

       points that overlap the edges are considered
       """

       pythag = lambda x, y: math.sqrt(math.pow(x, 2) + math.pow(y, 2))
       rr = self.radius - 1

       out = []
       for x in range(ctr_x - rr, ctr_x + rr + 1):
           for y in range(ctr_y - rr, ctr_y + rr + 1):
               if rr >= pythag(ctr_x-x, ctr_y-y):
                   out.append((x,y))

       return out

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
