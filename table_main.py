from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style

from zen_table import ZenTable
from button_bar import ButtonBar
from boustrophedon_solver import BoustrophedonSolver

TBL_WIDTH=600
TBL_HEIGHT=600
BALL_RADIUS=3


def main():
   root = Tk()
   root.resizable(0, 0)
   
   frame_t = Frame(root)
   frame_t.pack(fill=BOTH, expand=False)

   table = ZenTable(frame_t, TBL_WIDTH, TBL_HEIGHT)
      
   def solve_boustrophedon():
      print "--------------" #
      #table.debug()
      bs = BoustrophedonSolver(table.get_rockpoint(), 
                               table.get_drawing_area(),
                               BALL_RADIUS)
      bs.solve()


   buttons = ButtonBar(root, solve_boustrophedon)
   root.mainloop()



if __name__ == "__main__":
   main()
