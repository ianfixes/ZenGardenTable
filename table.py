from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style

TBL_WIDTH=600
TBL_HEIGHT=600

class ZenTable(Frame):
   """
   a UI element that allows drawing, then is drawn upon
   """

   def __init__(self, parent):
      Frame.__init__(self, parent)
      self.parent = parent
      self.initUI()
      self.pack()
      self.rockpoint = [[False for y in range(TBL_HEIGHT)] for x in range(TBL_WIDTH)]

   def initUI(self):
      self.b1up = True
      
      drawing_area = Canvas(self.parent, width=TBL_WIDTH, height=TBL_HEIGHT)
      drawing_area.pack(fill=BOTH, expand=1)
      drawing_area.bind("<Motion>",          self.h_motion)
      drawing_area.bind("<ButtonPress-1>",   self.h_b1down)
      drawing_area.bind("<ButtonRelease-1>", self.h_b1up)

      self.drawing_area = drawing_area

      self.pack(fill=BOTH, expand=1)

   def get_rockpoint(self):
      # copy the 2D array of rock points
      return [row[:] for row in self.rockpoint]

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
         
            event.widget.create_line(event.x,
                                     event.y,
                                     event.x+1,
                                     event.y+1,
                                     smooth=False,
                                     fill="red")
         except IndexError:
            print "Ignoring %s, %s" % (event.x, event.y)
      
         
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

class BoustrophedonSolver(object):
   def __init__(self, rockpoint_array):
      self.rockpoint = rockpoint_array

   def solve(self):
      print "SOLVING IT"


class ButtonBar(Frame):
   def __init__(self, parent, on_ok=None):
      Frame.__init__(self, parent, relief=RAISED, borderwidth=1)
      self.parent = parent
      self.on_ok = on_ok

      self.pack()
      self.initUI()

   def initUI(self):
      self.style = Style()
      self.style.theme_use("default")

      close_button = Button(self, text="Close")
      close_button.pack(side=RIGHT, padx=5, pady=5)
      close_button.bind("<ButtonRelease-1>", self.h_close)

      ok_button = Button(self, text="OK")
      ok_button.pack(side=RIGHT)
      ok_button.bind("<ButtonRelease-1>", self.h_ok)

      self.pack(fill=BOTH, expand=False)

   def h_close(self, event):
      self.parent.destroy()

   def h_ok(self, event):
      if self.on_ok: 
         self.on_ok()
      print "ButtonBar.h_ok is done"

def main():
   root = Tk()
   root.resizable(0, 0)
   
   frame_t = Frame(root)
   frame_t.pack(fill=BOTH, expand=False)

   table = ZenTable(frame_t)
      
   def solve_boustrophedon():
      #table.debug()
      bs = BoustrophedonSolver(table.get_rockpoint())
      bs.solve()


   buttons = ButtonBar(root, solve_boustrophedon)
   root.mainloop()



if __name__ == "__main__":
   main()
