try:
  import tkinter as tk
  from tkinter import ttk
except ImportError:
  import Tkinter as tk
  from Tkinter import ttk

#------------------------------
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
#------------------------------
try:
    import json
except ImportError:
    import simplejson as json
#------------------------------
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('<name of json file from enabling Google Drive API and Google Sheets API>', scope)
client = gspread.authorize(creds)
sheet = client.open('<name of your google sheet here.>').sheet1
#------------------------------
userName = None
#------------------------------
def NavTo(cntrl, page):
  cntrl.show_frame(page)

def PopulateData(dl):
  for data in range(len(GetData(userName))):
    dl.insert(data,GetData(userName)[data][0])

def HandlePopUp(uN, pW, pU, cPW):
  if(pW.get() == cPW):
    global userName
    userName = uN.get()
    pU.destroy()
    SignUp(uN.get(), pW.get())
    pW.delete(0, 'end')
  else:
    pU.destroy()

def PopUpMsg(uN, pW, msg):
  popUp = tk.Tk()
  popUp.wm_title("Confirm")
  msgLabel = tk.Label(popUp, text = msg)
  msgLabel.pack(side="top", fill = "x", pady = 5, padx = 5)
  _pWEnt = tk.Entry(popUp, show = "*")
  _pWEnt.pack()
  confirmBtn = tk.Button(popUp, text = "Ok", command = lambda:HandlePopUp(uN, pW, popUp, _pWEnt.get()))
  confirmBtn.pack()
  popUp.mainloop()

def set_text(e, txt):
    e.insert(0,txt)
    return

def CallBack(obj):
  try:
    w = obj.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    ViewData(index)
  except:
    print("Callback Method error.")

def ViewData(index):
  index = str(index)
  ED = tk.Tk()
  global userName
  dataDic = GetData(userName)
  ED.wm_title(dataDic[index]["Title"] + "Data")
  #------------------------------
  title = tk.Label(ED, text = "Title:")
  _title = tk.Entry(ED)
  print(index)
  set_text(_title, dataDic[index]["Title"])
  #------------------------------
  userN = tk.Label(ED, text = "Username:")
  _userN = tk.Entry(ED)
  set_text(_userN, dataDic[index]["Username"])
  #------------------------------
  passW = tk.Label(ED, text = "Password:")
  _passW = tk.Entry(ED)
  set_text(_passW, dataDic[index]["Password"])
  #------------------------------
  title.grid(row=0, sticky = "e")
  _title.grid(row=0, column = 1)
  #------------------------------
  userN.grid(row = 1, sticky = "e")
  _userN.grid(row = 1, column = 1)
  #------------------------------
  passW.grid(row = 2, sticky = "e")
  _passW.grid(row = 2, column = 1)
  #------------------------------
  saveData = tk.Button(ED, text = "Save", command = lambda:UpdateData(_title.get(), _userN.get(), _passW.get(), index))
  saveData.grid(row=3, columnspan = 2)
  #------------------------------
  ED.resizable(False,False)
  ED.mainloop()

def CreateDataPage():
  DP = tk.Tk()
  DP.geometry("275x285")
  DP.wm_title("Data Storage")
  
  dataList = tk.Listbox(DP)
  dataList.grid(row=0, columnspan = 2, sticky= "nsew")
  dataList.bind('<<ListboxSelect>>', CallBack)
  global userName
  for k, v in GetData(userName).items():
    dataList.insert(k, v["Title"])
  #------------------------------
  title = tk.Label(DP, text = "Title:")
  _title = tk.Entry(DP)
  #------------------------------
  userN = tk.Label(DP, text = "Username:")
  _userN = tk.Entry(DP)
  #------------------------------
  passW = tk.Label(DP, text = "Password:")
  _passW = tk.Entry(DP)
  #------------------------------
  title.grid(row=1, sticky = "e")
  _title.grid(row=1, column = 1)
  #------------------------------
  userN.grid(row = 2, sticky = "e")
  _userN.grid(row = 2, column = 1)
  #------------------------------
  passW.grid(row = 3, sticky = "e")
  _passW.grid(row = 3, column = 1)
  #------------------------------
  addData = tk.Button(DP, text = "Add Data", command = lambda:AddData(_title.get(), _userN.get(),_passW.get(),DP))
  addData.grid(row=4, columnspan = 2)
  #------------------------------
  DP.resizable(False,False)
  DP.mainloop()

def GetData(uN):
  dataDic = {}
  for x in range(2, sheet.row_count+1):
    if(sheet.cell(x,1).value == uN):
      if(sheet.cell(x,3).value != ""):
        dataDic = json.loads(sheet.cell(x,3).value)
  return dataDic

def UpdateData(t, u, p, i):
  global userName
  dataDic = GetData(userName)
  for k, v in dataDic.items():
    if (k == i):
      v["Title"] = t
      v["Username"] = u
      v["Password"] = p
    for x in range(2,sheet.row_count+1):
      if (sheet.cell(x,1).value == userName):
        data = json.dumps(dataDic)
        sheet.update_cell(x,3, data)

def AddData(t, u, p, dP):
  dP.destroy()
  dataDic = {}
  dataDic["Title"] = t
  dataDic["Username"] = u
  dataDic["Password"] = p
  global userName
  eData = GetData(userName)

  for x in range(2,sheet.row_count+1):
    if (sheet.cell(x,1).value == userName):
      eData[len(eData)] = dataDic
      data = json.dumps(eData)
      sheet.update_cell(x,3, data)
  CreateDataPage()

def LogIn(uN, pW):
  for x in range(2,sheet.row_count+1):
    if (sheet.cell(x,1).value == uN.get()):
      print("Username correct!")
      global userName
      userName = uN.get()
      if (sheet.cell(x,2).value == pW.get()):
        print("Password correct!")
        pW.delete(0, 'end')
        CreateDataPage()
        break

def SignUp(uN, pW):
  for x in range(2, sheet.row_count+1):
    if (sheet.cell(x, 1).value == uN):
      print("username already exists")
    elif(x == sheet.row_count):
      global userName
      userName = uN
      row = [uN, pW]
      index = int(sheet.row_count)
      sheet.insert_row(row, index)
      CreateDataPage()
      print("added user.")
    else:
      print("did nothing")
#------------------------------