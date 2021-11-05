import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()

#https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python