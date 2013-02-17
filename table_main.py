from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style

from zen_table import ZenTable


TBL_WIDTH=600
TBL_HEIGHT=600


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

   table = ZenTable(frame_t, TBL_WIDTH, TBL_HEIGHT)
      
   def solve_boustrophedon():
      #table.debug()
      bs = BoustrophedonSolver(table.get_rockpoint())
      bs.solve()


   buttons = ButtonBar(root, solve_boustrophedon)
   root.mainloop()



if __name__ == "__main__":
   main()
