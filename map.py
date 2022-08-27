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
        node1:Node = self.mapping[n1]
        node2:Node = self.mapping[n2]
        no = list(set(node1.no),set(node2.no))
        edge1 = Edge(n2,no=no)
        edge2 = Edge(n1,no=no)
        self.edges[n1].append(edge1)
        self.edges[n2].append(edge2)
    
    def Dijkstra(self,src:str,dst:str):
        src_index = self.mapping(src)
        dst_index = self.mapping(dst)
        self.distArr = np.ones((len(self.nodes),)) * INT_MAX
        self.visited = np.zeros((len(self.nodes),))
        self.pathRecord = np.zeros((len(self.nodes),))
        self.distArr[src_index] = 0

        for i in range(len(self.nodes)):
            minimum = INT_MAX 
            pos = -1 
            # find the minimum distance in the nodes left 
            for j in range(len(self.nodes)):
                if not self.visited[j] and self.distArr[j] < minimum:
                    minimum = self.distArr 
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
        
        self.shortestPath.append(dst_index)
        temp = self.pathRecord[dst_index]
        while temp != src_index:
            self.shortestPath.append(temp) 
            temp = self.pathRecord[temp]
        self.shortestPath.append(src_index)
        self.shortestPath.reverse()
