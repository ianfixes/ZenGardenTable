from Tkinter import Tk, Canvas, RIGHT, BOTH, RAISED
from ttk import Frame, Button, Style


class ButtonBar(Frame):

    def __init__(self, parent, on_ok=None, on_reset=None):
        Frame.__init__(self, parent, relief=RAISED, borderwidth=1)
        self.parent   = parent
        self.on_ok    = on_ok
        self.on_reset = on_reset

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

        rs_button = Button(self, text="Reset")
        rs_button.pack(side=RIGHT)
        rs_button.bind("<ButtonRelease-1>", self.h_rst)

        self.pack(fill=BOTH, expand=False)

    def h_close(self, event):
        self.parent.destroy()

    def h_ok(self, event):
        if self.on_ok: self.on_ok()

    def h_rst(self, event):
        if self.on_reset: self.on_reset()
