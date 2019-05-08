try:
  import tkinter as tk
except ImportError:
  import Tkinter as tk
#------------------------------
import LogInPage as lip
#------------------------------

class DataApp(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    tk.Tk.wm_title(self, "MyData")

    container = tk.Frame(self)
    container.pack(side="top", fill = "both", expand = True)
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    self.frames = {}

    for F in (lip.LogInPage,):
      frame = F(container, self)
      self.frames[F] = frame
      frame.grid(row = 0, column = 0, sticky = "nsew")

    self.show_frame(lip.LogInPage)
  #------------------------------
  def show_frame(self, cont):
    frame = self.frames[cont]
    frame.tkraise()

#------------------------------
app = DataApp()
app.geometry("275x80")
app.resizable(False,False)
app.mainloop()
#------------------------------