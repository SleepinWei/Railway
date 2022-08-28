from cgitb import text
from re import search
from socket import SO_RCVBUF
import tkinter as tk 
from tkinter import ttk as ttk 
from map import Edge, Map, Node,vec2
import numpy as np
class GUI():
    def __init__(self,window) -> None:
        self.root = window 
        self.content = ttk.Frame(self.root)
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.content.rowconfigure(0,weight=1)
        self.content.columnconfigure(0,weight=1)
        self.map = Map() 
    
    def setWindow(self):
        self.content.grid(column=0,row=0,sticky="news")
    
    def setCanvas(self):
        self.canvas = tk.Canvas(self.content)
        self.h = ttk.Scrollbar(self.content, orient=tk.HORIZONTAL)
        self.v = ttk.Scrollbar(self.content, orient=tk.VERTICAL)

        # size
        self.canvas["width"] = 1000
        self.canvas["height"] = 600
        self.canvas["scrollregion"] = (0, 0, 4000, 4000)
        self.canvas.yview_moveto(0.25)
        self.canvas.xview_moveto(0.25)
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
    
    def drawMap(self):
        map = self.map 

        
        def on_enter(e):
            self.canvas.config(cursor="hand2")
        
        def on_leave(e):
            self.canvas.config(cursor="")
        
        def on_click(e):
            # 点击选择节点信息
            pass
        
        def drawNode(node:Node):
            R = 5 
            text_w = R - 1
            text_h = R + 3 
            l = self.canvas.create_oval(node.pos.x-R,node.pos.y-R,node.pos.x + R ,node.pos.y + R ,
                fill="yellow",outline="purple",tags=("nodes",node.name))
            text = self.canvas.create_text(node.pos.x - text_w,node.pos.y - text_h,text=node.name
                )
            self.canvas.tag_bind(l,"<Enter>",on_enter)
            self.canvas.tag_bind(l,"<Leave>",on_leave)
        
        def drawEdge(nodefrom:Node, edge:Edge):
            pos1=  nodefrom.pos
            pos2 = map.nodes[edge.to].pos
            l = self.canvas.create_line(pos1.x,pos1.y,pos2.x,pos2.y,fill="black",smooth=True,
            tags=("edge",nodefrom.name,map.nodes[edge.to].name))
            self.canvas.tag_bind(l,"<Enter>",on_enter)
            self.canvas.tag_bind(l,"<Leave>",on_leave)

        for node in map.nodes:
            drawNode(node)

        # visited = np.zeros((len(map.nodes)))
        for i in range(len(map.nodes)):
            n = map.nodes[i]
            # 画两遍，如何解决？
            for edge in map.edges[i]:
                drawEdge(n,edge)

    def setInputFrame(self):
        self.inputFrame = ttk.LabelFrame(self.content,text="Input")
        # self.label1 = ttk.Label(self.inputFrame,text="节点信息")

        self.stationFrame = ttk.LabelFrame(self.inputFrame, text="站点")
        self.label3 = ttk.Label(self.stationFrame,text="名称")
        self.namevariable = tk.StringVar(value="C")
        self.nameEntry = ttk.Entry(self.stationFrame,textvariable=self.namevariable)
        self.label4 = ttk.Label(self.stationFrame,text="线路")
        self.novariable = tk.StringVar(value="3")
        self.noEntry = ttk.Entry(self.stationFrame,textvariable=self.novariable)
        self.label5 = ttk.Label(self.stationFrame,text="坐标")
        self.posVariable = tk.StringVar(value="100 200")
        self.posEntry = ttk.Entry(self.stationFrame,textvariable=self.posVariable)

        self.edgeFrame = ttk.LabelFrame(self.inputFrame,text="边")
        self.srcVariable = tk.StringVar(value="B")
        self.dstVariable = tk.StringVar(value="C")
        self.srcEntry = ttk.Entry(self.edgeFrame,textvariable=self.srcVariable)
        self.dstEntry = ttk.Entry(self.edgeFrame,textvariable=self.dstVariable)

        def parseNo(string:str):
            temp = string.strip().split(" ")
            no = [int(i) for i in temp]
            return no
        
        def parsePos(string:str):
            temp = string.strip().split(" ")
            return vec2(float(temp[0]),float(temp[1]))

        def addNode():
            name = self.nameEntry.get()
            no = parseNo(self.noEntry.get())
            pos = parsePos(self.posEntry.get())
            self.map.addNode(name,pos,no)
            self.canvas.delete(tk.ALL)
            self.drawMap()
            
        def addEdge():
            src = self.srcEntry.get().strip()
            dst = self.dstEntry.get().strip()
            self.map.addEdge(src,dst)
            self.canvas.delete(tk.ALL)
            self.drawMap()

        self.addNodeButton = ttk.Button(self.stationFrame,text="添加站点",command=addNode)
        self.addEdgeButton = ttk.Button(self.edgeFrame,text="添加边",command=addEdge)
    
        # 路径规划
        self.pathFrame = ttk.LabelFrame(self.inputFrame,text="地铁换乘")
        self.label6 = ttk.Label(self.pathFrame,text="起点")
        self.label7 = ttk.Label(self.pathFrame,text="终点")
        self.srcStation = tk.StringVar(value="A")
        self.srcStationEntry = ttk.Entry(self.pathFrame,textvariable=self.srcStation)
        self.dstStation = tk.StringVar(value="C")
        self.dstStationEntry = ttk.Entry(self.pathFrame,textvariable=self.dstStation)
        self.pathText = tk.Text(self.pathFrame,width=7,height=7)

        def searchPath():
            src = self.srcStationEntry.get().strip()
            dst = self.dstStationEntry.get().strip()
            self.map.Dijkstra(src,dst)
            def pathToString(path):
                s = "" 
                for name in path: 
                    s+=name 
                    s+='\n'
                return s
            self.pathText.delete("0.0","end")
            self.pathText.insert("0.0",pathToString(self.map.shortestPath))

        self.searchButton = ttk.Button(self.pathFrame,text="规划路径",command=searchPath)
        
        # layout 

        self.inputFrame.grid(column=2,row=0,sticky="news")
        # self.label1.grid(column=0,row=0,sticky="nws")
        self.stationFrame.grid(column=0,row=1,sticky="nws")
        self.label3.grid(column=0,row=1,sticky="nws")
        self.nameEntry.grid(column=1,row=1,sticky="nws")
        self.label4.grid(column=0,row=2,sticky="nws")
        self.noEntry.grid(column=1,row=2,sticky="nws")
        self.label5.grid(column=0,row=3,sticky="nws")
        self.posEntry.grid(column=1,row=3,sticky="nws")
        self.addNodeButton.grid(column=0,row=4,sticky="nws")

        self.edgeFrame.grid(column=0,row=2,sticky="nws")
        self.srcEntry.grid(column=0,row=6,sticky="nws")
        self.dstEntry.grid(column=1,row=6,sticky="nws")
        self.addEdgeButton.grid(column=0,row=7,sticky="nws")
    
        self.pathFrame.grid(column=0,row=0,sticky="news")
        self.label6.grid(column=0,row=0,sticky="nws")
        self.label7.grid(column=0,row=1,sticky="nws")
        self.srcStationEntry.grid(column=1,row=0,sticky="nws")
        self.dstStationEntry.grid(column=1,row=1,sticky="nws")
        self.searchButton.grid(column=0,row=2,sticky="nws")
        self.pathText.grid(column=0,columnspan=2,row=3,sticky="nwes")
    def run(self):
        self.setWindow() 
        self.setCanvas()
        self.setInputFrame()
        self.map.fromFile("./node1.txt","./edge1.txt")
        self.drawMap()
        self.root.mainloop()


if __name__ == "__main__":
    window = tk.Tk() 
    window.title("Shanghai Railway")
    window.geometry("800x600")
    gui = GUI(window)
    gui.run()