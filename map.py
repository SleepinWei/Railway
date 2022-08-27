import numpy as np 

INT_MAX = 1e6 

class vec2():
    def __init__(self) -> None:
        self.x = 0 
        self.y = 0

class Node():
    def __init__(self) -> None:
        self.name : str = "" 
        self.no = [] # 属于几号线
        # self.color = 0 
        self.pos = vec2() 

class Edge():
    def __init__(self) -> None:
        # self.nodes = vec2() # 两端连接的节点，站点名称
        self.to:int = 0 # 有向边指向的序号
        self.dist:float = 0 
        self.no: int = 0  # 属于几号线

class Map():
    def __init__(self) -> None:
        self.nodes = [] 
        self.edges = [] # 邻接链表 （二维）Edge 类型
        self.mapping = dict() # 站名-> index of node
        self.shortestPath = [] 
        self.distArr = np.zeros((len(self.nodes),))
        self.visited = np.zeros((len(self.nodes),))
    
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
