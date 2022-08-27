import tkinter as tk 
from tkinter import ttk as ttk 

class GUI():
    def __init__(self,window) -> None:
        self.root = window 
        self.content = ttk.Frame(self.root)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.content.rowconfigure(0,weight=1)
        self.content.columnconfigure(0,weight=1)
    
    def setWindow(self):
        self.content.grid(column=0,row=0,sticky="news")
    
    def setCanvas(self):
        self.canvas = tk.Canvas(self.content)
        self.h = ttk.Scrollbar(self.content, orient=tk.HORIZONTAL)
        self.v = ttk.Scrollbar(self.content, orient=tk.VERTICAL)

        # size
        self.canvas["width"] = 1000
        self.canvas["height"] = 600
        self.canvas["scrollregion"] = (0, 0, 2000, 2000)
        self.canvas.configure(background="LightCyan")

        # commands
        self.h["command"] = self.canvas.xview
        self.v["command"] = self.canvas.yview

        self.canvas["xscrollcommand"] = self.h.set
        self.canvas["yscrollcommand"] = self.v.set

        # layout
        self.canvas.grid(column=0, row=0, sticky="news")
        self.h.grid(column=0, row=1, sticky="we")
        self.v.grid(column=1, row=0, sticky="ns")
    
    def setInputFrame(self):
        self.inputFrame = ttk.LabelFrame(self.content,text="Input")
        self.label1 = ttk.Label(self.inputFrame,text="test label")
        
        # layout 
        self.inputFrame.grid(column=2,row=0,sticky="news")
        self.label1.grid(column=0,row=0,sticky="nws")
    
    def run(self):
        self.setWindow() 
        self.setCanvas()
        self.setInputFrame()
        self.root.mainloop()


if __name__ == "__main__":
    window = tk.Tk() 
    window.title("Shanghai Railway")
    window.geometry("600x600")
    gui = GUI(window)
    gui.run()