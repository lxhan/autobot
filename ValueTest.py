from Tkinter import *
import BasicActions

ba = BasicActions

root = Tk()
v = IntVar()


class Test(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        Label(root, text="""Select something""", justify=LEFT, padx=20).pack()
        Radiobutton(root, text="Option 1", padx=20, variable=v, value=1).pack(anchor=W)
        Radiobutton(root, text="Option 2", padx=20, variable=v, value=2).pack(anchor=W)
        Button(root, text="OK", command=self.select_val).pack()

    def select_val(self):
        x = v.get()


app = Test(master=root)
app.mainloop()
