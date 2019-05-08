try:
  import tkinter as tk
except ImportError:
  import Tkinter as tk
#------------------------------
import Globals as glbl
#------------------------------

class LogInPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    #------------------------------
    userN = tk.Label(self, text = "Username:")
    _userN = tk.Entry(self)
    #------------------------------
    passW = tk.Label(self, text = "Password:")
    _passW = tk.Entry(self, show = "*")
    #------------------------------
    userN.grid(row = 0, sticky = "e")
    _userN.grid(row = 0, column = 1)
    #------------------------------
    passW.grid(row = 1, sticky = "e")
    _passW.grid(row = 1, column = 1)
    #------------------------------
    logIn = tk.Button(self, text = "Log in", command = lambda: glbl.LogIn(_userN, _passW))
    logIn.grid(row=2, column = 1)
    #------------------------------
    signUp = tk.Button(self, text = "Sign up", command = lambda: glbl.PopUpMsg(_userN, _passW, "Please re-enter the password to confirm."))
    signUp.grid(row=2, column = 0)
    #------------------------------
