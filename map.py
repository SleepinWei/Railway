import numpy as np 
from geopy.distance import geodesic

INT_MAX = 1e6 
def colorchange(a,b,c):
    stringa = hex(a)[2:]
    if len(stringa) == 1:
        stringa = "0" + stringa 
    stringb = hex(b)[2:]
    if len(stringb) == 1:
        stringb = "0"+ stringb
    stringc = hex(c)[2:]
    if len(stringc) == 1:
        stringc = "0"+ stringc
    return f"#{stringa}{stringb}{stringc}"
COLOR = {
    1:colorchange(231,0,18),
    2:colorchange(155,204,1),
    3:colorchange(255,209,2),
    4:colorchange(121,99,163),
    5:colorchange(149,72,154),
    6:colorchange(213,0,99),
    7:colorchange(231,109,0),
    8:colorchange(28,142,194),
    9:colorchange(137,204,233),
    10:colorchange(198,172,211),
    11:colorchange(145,69,69),
    12:colorchange(39,146,116),
    13:colorchange(255,157,196),
    14:colorchange(153,163,66),
    15:colorchange(190,165,134),
    16:colorchange(151,208,191),
    17:colorchange(174,125,118),
    18:colorchange(220,173,115),
    19:colorchange(177,177,177),
    20:colorchange(232,148,86),
    21:colorchange(61,61,61),
    22:colorchange(0,0,0)
}

class vec2():
    def __init__(self,x=0,y=0) -> None:
        self.x = x 
        self.y = y

class Node():
    def __init__(self,name="",no =[],pos = vec2(0,0),apos:vec2 = vec2(0,0)) -> None:
        self.name : str = name
        self.no = no# 属于几号线 list() 
        # self.color = 0 
        self.pos = pos 
        self.apos = apos  # x: 经度 y : 纬度
        self.onPath = 0

class Edge():
    def __init__(self,to=0,dist=0,no=0) -> None:
        # self.nodes = vec2() # 两端连接的节点，站点名称
        self.to:int = to # 有向边指向的序号
        self.dist:float = dist 
        self.no = no  # 属于几号线

class Map():
    def __init__(self) -> None:
        self.nodes = [] 
        self.edges = [] # 邻接链表 （二维）Edge 类型
        self.mapping = dict() # 站名-> index of node
        self.shortestPath = [] 
        self.distArr = np.zeros((len(self.nodes),))
        self.visited = np.zeros((len(self.nodes),))
    
    def addNode(self,name:str,apos:vec2,no):
        if name in list(self.mapping.keys()):
            node:Node = self.nodes[self.mapping[name]]
            node.no.append(int(no[0]))
        else:
            node = Node(name,apos=apos,no=no)
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
            return geodesic((p1.y,p1.x),(p2.y,p2.x)).m

        edge1.dist = distance(node1.apos,node2.apos) 
        edge2.dist = edge1.dist
        self.edges[self.mapping[n1]].append(edge1)
        self.edges[self.mapping[n2]].append(edge2)
    
    def fromFile(self,nodefile,edgefile):
        file = open(nodefile,"r")
        lines = file.readlines()

        for line in lines:
            el = line.strip().split(" ")
            name = el[0] 
            apos = vec2(float(el[1]),float(el[2]))
            no = el[3:]
            no = [int(i) for i in no]
            self.addNode(name,apos=apos,no=no)
        file.close()

        file = open(edgefile,"r")
        lines = file.readlines()
        for line in lines:
            el = line.strip().split(" ")
            n1 = el[0]
            n2 = el[1] 
            self.addEdge(n1,n2)
        file.close()
        # 计算 像素位置 pos
        minimum_x = INT_MAX 
        maximum_x = 0 
        minimum_y = INT_MAX
        maximum_y = 0  
        for node in self.nodes:
            minimum_x = min(minimum_x,node.apos.x)
            maximum_x = max(maximum_x,node.apos.x)
            minimum_y = min(minimum_y,node.apos.y)
            maximum_y = max(maximum_y,node.apos.y)
        
        for node in self.nodes:
            t_x= 2500 / (maximum_x - minimum_x)
            t_y = 2500 / (maximum_y - minimum_y)
            t = max(t_x,t_y)
            interval = 20
            node.pos = vec2(y=4000-(node.apos.y - minimum_y) * t - interval,x=(node.apos.x - minimum_x) * t + interval)
    
    def Dijkstra(self,src:str,dst:str):
        # 初始化
        self.shortestPath = [] 
        for node in self.nodes:
            node.onPath = 0

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
        self.nodes[dst_index].onPath = 1 
        # print(self.pathRecord)
        while temp != src_index:
            self.nodes[temp].onPath = 1
            self.shortestPath.append(self.nodes[temp].name) 
            temp = int(self.pathRecord[temp])
        self.shortestPath.append(self.nodes[src_index].name)
        self.nodes[src_index].onPath = 1
        self.shortestPath.reverse()

if __name__ == "__main__":
    print(colorchange(123,2,4))