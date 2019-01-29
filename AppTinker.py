from Tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def say_hi(self):
        print("Hi hi hi!")

    def create_widgets(self):
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello World"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

root = Tk()
app = Application(master=root)
app.mainloop()
