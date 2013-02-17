from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style

from zen_table import ZenTable
from button_bar import ButtonBar
from boustrophedon_solver import BoustrophedonSolver

TBL_WIDTH=600
TBL_HEIGHT=600


class BoustrophedonSolver(object):
   def __init__(self, rockpoint_array):
      self.rockpoint = rockpoint_array

   def solve(self):
      print "SOLVING IT"


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
