from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style

from zen_table import ZenTable
from button_bar import ButtonBar
from boustrophedon_solver import BoustrophedonSolver
from contour_solver import ContourSolver
from ball import Ball
from background import LinearBackground

from sand_ripple import SandRipple

TBL_WIDTH=200
TBL_HEIGHT=200
BALL_RADIUS=10


def main():
    root = Tk()
    root.resizable(0, 0)

    frame_t = Frame(root)
    frame_t.pack(fill=BOTH, expand=False)

    table = ZenTable(frame_t, TBL_WIDTH, TBL_HEIGHT)

    ball = Ball(BALL_RADIUS)
    bs = BoustrophedonSolver(table, ball)
    cs = ContourSolver(table, ball, bs.is_rockpoint)
    bg = LinearBackground(table, ball)

    def solve_boustrophedon():
        print "--------------" #
        #table.debug()
        bs.solve()
        #bs.animate_path(15)
        bs.show_covered_points()
        bs.show_visited_points()
        cs.solve(bs.get_visited_list(), 3)
        cs.draw_contours()
        bg.solve(bs.get_visited_list(), dict([(p, v is not None) for (p, v) in cs.proximity_map.iteritems()]))
        bg.draw()


    def on_reset():
        bs.stop_animating()
        table.resetSimulation()


    def draw_ripples():
        rip = SandRipple(TBL_WIDTH, TBL_HEIGHT)
        for i in range(200):
            print "Iteration #", i
            rip.iterate(20.0, 0.5, 0.0, 0.0, 0.1, 0.8, 0, 1)

            for x, col in enumerate(rip.normalize(255)):
                for y, val in enumerate(col):
                    myColor = "#%0.2x%0.2x%0.2x" % ((val,) * 3)
                    table.draw_point(x, y, myColor)
            table.drawing_area.update_idletasks()

            
    buttons = ButtonBar(root, solve_boustrophedon, on_reset) # do the explorer
    #buttons = ButtonBar(root, draw_ripples, table.resetSimulation)        # do the sand ripple sim
    root.mainloop()



if __name__ == "__main__":
   main()
