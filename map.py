from math import sqrt
import numpy as np 

INT_MAX = 1e6 

class vec2():
    def __init__(self,x=0,y=0) -> None:
        self.x = x 
        self.y = y

class Node():
    def __init__(self,name="",no =[],pos = vec2(0,0)) -> None:
        self.name : str = name
        self.no = no# 属于几号线 list() 
        # self.color = 0 
        self.pos = pos 

class Edge():
    def __init__(self,to=0,dist=0,no=0) -> None:
        # self.nodes = vec2() # 两端连接的节点，站点名称
        self.to:int = to # 有向边指向的序号
        self.dist:float = dist 
        self.no = []  # 属于几号线

class Map():
    def __init__(self) -> None:
        self.nodes = [] 
        self.edges = [] # 邻接链表 （二维）Edge 类型
        self.mapping = dict() # 站名-> index of node
        self.shortestPath = [] 
        self.distArr = np.zeros((len(self.nodes),))
        self.visited = np.zeros((len(self.nodes),))
    
    def addNode(self,name:str,pos:vec2,no):
        node = Node(name,pos=pos,no=no)
        self.nodes.append(node)
        self.mapping.update({name:len(self.nodes)-1})
        self.edges.append([])
    
    def addEdge(self,n1:str,n2:str):
        index1 = self.mapping[n1]
        index2 = self.mapping[n2]
        node1:Node = self.nodes[index1]
        node2:Node = self.nodes[index2]
        no = list(set(node1.no)&set(node2.no))
        edge1 = Edge(index2,no=no)
        edge2 = Edge(index1,no=no)

        def distance(p1:vec2,p2:vec2):
            return sqrt((p1.x - p2.x)**2 + (p1.y-p2.y)**2)

        edge1.dist = distance(node1.pos,node2.pos) 
        edge2.dist = edge1.dist
        self.edges[self.mapping[n1]].append(edge1)
        self.edges[self.mapping[n2]].append(edge2)
    
    def fromFile(self,nodefile,edgefile):
        file = open(nodefile,"r")
        lines = file.readlines()

        for line in lines:
            el = line.strip().split(" ")
            name = el[0] 
            pos = vec2(float(el[1]),float(el[2]))
            no = el[3:]
            self.addNode(name,pos,no)
        
        file.close()

        file = open(edgefile,"r")
        lines = file.readlines()
        for line in lines:
            el = line.strip().split(" ")
            n1 = el[0]
            n2 = el[1] 
            self.addEdge(n1,n2)
    
    def Dijkstra(self,src:str,dst:str):
        src_index = self.mapping[src]
        dst_index = self.mapping[dst]
        self.distArr = np.ones(len(self.nodes)) * INT_MAX
        self.visited = np.zeros(len(self.nodes))
        self.pathRecord = np.zeros(len(self.nodes))
        self.distArr[src_index] = 0

        for i in range(len(self.nodes)):
            minimum = INT_MAX 
            pos = -1 
            # find the minimum distance in the nodes left 
            for j in range(len(self.nodes)):
                if (not self.visited[j]) and (self.distArr[j] < minimum):
                    minimum = self.distArr[j]
                    pos = j 
            if pos == -1 : 
                break # 不连通

            self.visited[pos] = 1 
            for j in range(len(self.edges[pos])):
                distedge = self.edges[pos][j]
                if not self.visited[distedge.to]:
                    # if not visited, then update weight
                    if self.distArr[distedge.to] > self.distArr[pos] + self.edges[pos][j].dist:
                        self.distArr[distedge.to] = self.distArr[pos] + self.edges[pos][j].dist 
                        self.pathRecord[distedge.to] = pos
        
        self.shortestPath.append(self.nodes[dst_index].name)
        temp = int(self.pathRecord[dst_index])
        # print(self.pathRecord)
        while temp != src_index:
            self.shortestPath.append(self.nodes[temp].name) 
            temp = int(self.pathRecord[temp])
        self.shortestPath.append(self.nodes[src_index].name)
        self.shortestPath.reverse()

if __name__ == "__main__":
    m = Map()
    m.fromFile("./node.txt","./edge.txt")
    print(m.mapping)