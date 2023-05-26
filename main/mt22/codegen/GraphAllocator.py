class GraphAllocator():
    
    def __init__(self, unique_id_list, flow):
        self.unique_id_list = unique_id_list
        self.flow = flow
        self.V = len(unique_id_list)
        self.color_global = [0] * self.V
        self.graph = [[0 for _ in range(self.V)] for _ in range(self.V)]
        
    def flowToAdj(self):
        for i in range(0,len(self.flow)):
            for j in range(0,len(self.flow[i])):
                for k in range(0,len(self.flow[i])):
                    self.graph[self.unique_id_list.index(self.flow[i][j])][self.unique_id_list.index(self.flow[i][k])]=1	#For variables appearing together in a tuple, introduces an edge in the graph 
        # remove auto-loop
        for i in range(0,self.V):
            self.graph[i][i]=0
        return self.graph

	# Check for Neighbors if they have the same color
    def isNeighborColor(self, v, color, c):
        for i in range(self.V):
            if self.graph[v][i] == 1 and color[i] == c:
                return True
        return False
	
    # Recursion to get number of colors needed
    def graphColorRecursionCheck(self, num_regs, color, v):
        if v == self.V:
            return True

        for c in range(1, num_regs+1):
            if self.isNeighborColor(v, color, c) == False:
                color[v] = c
                if self.graphColorRecursionCheck(num_regs, color, v+1) == True:
                    return True
                else: color[v] = -1
	
	# Coloring operation for graph
    def graphColoring(self, num_regs):
        color = [0] * self.V
        # if we cant color the list of vars with number of given regs
        if num_regs<=0 or self.graphColorRecursionCheck(num_regs, color, 0) == False and -1 in color:
            return False
        self.color_global = color
        return True