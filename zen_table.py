from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style


class ZenTable(Frame):
   """
   a UI element that allows drawing, then is drawn upon
   """

   def __init__(self, parent, table_width, table_height):
       Frame.__init__(self, parent)
       self.parent = parent
       self.table_width = table_width
       self.table_height = table_height
       self.initUI()
       self.pack()
       self.rockpoint = [[False for y in range(self.table_height)] for x in range(self.table_width)]

   def initUI(self):
       self.b1up = True

       drawing_area = Canvas(self.parent, width=self.table_width, height=self.table_height)
       drawing_area.pack(fill=BOTH, expand=1)
       drawing_area.xview("moveto", 0) # http://tcl.sourceforge.net/faqs/tk/#canvas/border
       drawing_area.yview("moveto", 0)
       drawing_area.bind("<Motion>",          self.h_motion)
       drawing_area.bind("<ButtonPress-1>",   self.h_b1down)
       drawing_area.bind("<ButtonRelease-1>", self.h_b1up)

       self.drawing_area = drawing_area

       self.pack(fill=BOTH, expand=1)

   def get_rockpoint(self):
       # copy the 2D array of rock points
       return [row[:] for row in self.rockpoint]

   def get_drawing_area(self):
       return self.drawing_area

   def h_b1down(self, event):
       # we only want to draw when the button is down
       # because "Motion" events happen -all the time-
       self.b1up = False
       self.reg_point(event)

   def h_b1up(self, event):
       self.b1up = True

   def h_motion(self, event):
       self.reg_point(event)

   def reg_point(self, event):
       if not self.b1up:
           try:
               self.rockpoint[event.x][event.y] = True
               self.draw_point(event)
           except IndexError:
               print "Ignoring %s, %s" % (event.x, event.y)


   def draw_point(self, event):
       x = event.x
       y = event.y

#       # diagonal pair
#       event.widget.create_line(x, y, x+1, y+1, smooth=False, fill="red")

      # 3x3
       for yy in range(y-1, y+2):
           event.widget.create_line(x-1, yy, x+1, yy, smooth=False, fill="red")


   def debug(self):
       for x, col in enumerate(self.rockpoint):
           for y, is_point in enumerate(col):
               if is_point:
                   print "point at %d, %d" % (x, y)

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

           self.drawing_area.create_line(p, p, np, np, smooth=False, fill="blue")
           self.animation_steps = np

         #self.update_idletasks()

           self.after(100, self.draw_frame)
