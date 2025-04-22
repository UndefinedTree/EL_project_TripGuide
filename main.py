answer = input("Hello, can you see this? Please input 'yse' or 'no'")
if answer == "yes":
    print("OK, it's fine!")
else:
    print("Oh, there is sth wrong!")

from tkinter import *

class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.createWidegt()
    def createWidegt(self):
        pass

root = Tk()
root.geometry("500x300+500+300")
root.title("push test")
app = Application(master=root)
root.mainloop()