
from tkinter import *
from tkinter import messagebox


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.btn 01=Label(self,text='出发地：',bg='grey',font=('Arial',12),width=10,height=1)
        self.btn01.pack(side=LEFT)
        self.btn0101=Entry(self,width=20,font=('Arial',12))
        self.btn0101.pack()
        self.btn02=Button(self,text='退出',command=root.destroy)
        self.btn02.pack()

if __name__ == '__main__':
    root = Tk()
    root.geometry('1000x600+100+100')
    root.title('欢迎使用travel hamster~!')
    app = Application(master=root)
    root.mainloop()
