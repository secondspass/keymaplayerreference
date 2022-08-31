from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

class KbLayout:
    def __init__(self, root):
        self.root = root
        self.root.title("Redox keyboard layout")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.leftframe = ttk.Frame(self.mainframe, padding="1 1 1 1")
        self.leftframe.grid(column=0, row=0, sticky=W)
        self.layerbuttons = [
            ttk.Button(self.leftframe, text="L0", command=lambda: self.layer(0)),
            ttk.Button(self.leftframe, text="L1", command=lambda: self.layer(1)),
            ttk.Button(self.leftframe, text="L2", command=lambda: self.layer(2)),
            ttk.Button(self.leftframe, text="L3", command=lambda: self.layer(3)),
            ]
        for i, button in enumerate(self.layerbuttons):
            button.grid(column=0, row=i, sticky=W)
            self.leftframe.rowconfigure(i, weight=1)
        
        self.leftframe.columnconfigure(0, weight=1)

        self.rightframe = ttk.Frame(self.mainframe, padding="1 1 1 1")
        self.rightframe.grid(column=1, row=0, sticky=W)

        # the leftframe and rightframe are children of mainframe
        # leftframe sits on (0,0) and rightframe sits on (0,1) inside
        # mainframe's grid.
        # Setting weight=1 for rowconfigure and columnconfigure
        # will make sure that the frame's row and column size
        # at that particular grid location will resize with the window. 
        # setting weight=0 means that particular dimension will remain static
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=0)
        self.mainframe.columnconfigure(1, weight=1)

        self.layerimage  = Image.open("./images/layer0.png")
        self.max_width = self.layerimage.width
        self.max_height = self.layerimage.height
        self.layerdisplay = ImageTk.PhotoImage(self.layerimage)
        self.layerlabel = ttk.Label(self.rightframe, image=self.layerdisplay)
        self.layerlabel.grid(column=0,row=0,sticky=W)

        self.rightframe.rowconfigure(0, weight=1)
        self.rightframe.columnconfigure(0, weight=1)

        self.layerlabel.bind('<Configure>', self.resize_image)

    def layer(self, layernum):
        if layernum>3:
            return
        self.highlight_button(layernum)
        newlayerimage = Image.open("./images/layer{}.png".format(layernum) )
        newlayerimage = newlayerimage.resize((self.layerdisplay.width(), self.layerdisplay.height()))
        self.layerimage = newlayerimage
        self.layerdisplay = ImageTk.PhotoImage(self.layerimage)
        self.layerlabel['image'] = self.layerdisplay

    def highlight_button(self, layernum):
        for i in range(len(self.layerbuttons)):
            self.layerbuttons[i]['underline'] = -1
        self.layerbuttons[layernum]['underline'] = 1


    def resize_image(self, event):
        width = min(self.max_width, event.width)
        height = min(self.max_height, event.height)
        resized_image = self.layerimage.resize((width, height))
        self.layerdisplay = ImageTk.PhotoImage(resized_image)
        self.layerlabel['image'] = self.layerdisplay

if __name__ == '__main__':
    root = Tk()
    KbLayout(root)
    root.mainloop()
