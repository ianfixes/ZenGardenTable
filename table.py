from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style

class ZenTable(Frame):
   
   def __init__(self, parent):
      Frame.__init__(self, parent)
      self.parent = parent
      self.initUI()
      self.pack()

   def initUI(self):
      self.b1up = True
      self.xold = None
      self.yold = None
      
      self.parent.title("Buttons")
      
      #frame = Frame(self, relief=RAISED, borderwidth=1)
      #frame.pack(fill=BOTH, expand=1)

      drawing_area = Canvas(self.parent, width=600, height=600)
      drawing_area.pack(fill=BOTH, expand=1)
      drawing_area.bind("<Motion>",          self.h_motion)
      drawing_area.bind("<ButtonPress-1>",   self.h_b1down)
      drawing_area.bind("<ButtonRelease-1>", self.h_b1up)

      self.drawing_area = drawing_area

      self.pack(fill=BOTH, expand=1)
      
      self.style = Style()
      self.style.theme_use("default")
      closeButton = Button(self, text="Close")
      closeButton.pack(side=RIGHT, padx=5, pady=5)
      okButton = Button(self, text="OK")
      okButton.pack(side=RIGHT)


   def h_b1down(self, event):
      # we only want to draw when the button is down
      # because "Motion" events happen -all the time-
      self.b1up = False
      
   def h_b1up(self, event):
      self.b1up = True
      self.xold = None           # reset the line when you let go of the button
      self.yold = None

   def h_motion(self, event):
      if not self.b1up:
         if self.xold is not None and self.yold is not None:
            event.widget.create_line(self.xold,
                                     self.yold,
                                     event.x,
                                     event.y,
                                     smooth=False,
                                     fill="red")
                # here's where you draw it. smooth. neat.
         self.xold = event.x
         self.yold = event.y
            


def main():
    root = Tk()
    table = ZenTable(root)
    root.mainloop()


if __name__ == "__main__":
    main()
