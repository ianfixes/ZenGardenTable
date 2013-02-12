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
      
      drawing_area = Canvas(self.parent, width=600, height=600)
      drawing_area.pack(fill=BOTH, expand=1)
      drawing_area.bind("<Motion>",          self.h_motion)
      drawing_area.bind("<ButtonPress-1>",   self.h_b1down)
      drawing_area.bind("<ButtonRelease-1>", self.h_b1up)

      self.drawing_area = drawing_area

      self.pack(fill=BOTH, expand=1)

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
      

   buttons = ButtonBar(root, table.animate)
   root.mainloop()



if __name__ == "__main__":
   main()
