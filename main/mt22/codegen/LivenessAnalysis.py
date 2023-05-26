class LivenessAnalysis:
    def __init__(self, topology):
        self.topology = topology[1:]
        self.flow = []
        self.ids = []
        
    def getUniqueIds(self, out):
        for i in range(0,len(out)):
            for j in range(0,len(out[i])):
                if out[i][j] not in self.ids:
                    self.ids.append(out[i][j])
        return self.ids
        
    def createFlowGraph(self):
        out = [] # return
        temp = []
        temp2 = []
        print(self.topology)
        for i in range(0,len(self.topology)):
            # Prelim check: Add reused variables
            for next in range(i+1,len(self.topology)):
                # if reassigned
                if self.topology[i][0] == self.topology[next][0]: break
                # if reused
                elif self.topology[i][0] in self.topology[next]:
                    if self.topology[i][0] not in temp:
                        temp.append(self.topology[i][0])
                        break
            
            # Deep check: Add/Remove variables
            for j in range(1,len(self.topology[i])):
                if self.topology[i][j] not in temp:
                    temp.append(self.topology[i][j])
                # check: add all used vars into temp2
                for check_i in range(i+1,len(self.topology)):
                    for check_j in range(1,len(self.topology[check_i])):
                        temp2.append(self.topology[check_i][check_j])
                # check: remove all assigned vars
                for next in range(i+1,len(self.topology)):
                    # var is reassigned or var is never used again
                    if self.topology[i][j] == self.topology[next][0] or self.topology[i][j] not in temp2:
                        temp.remove(self.topology[i][j])
                        break
                temp2 = []
            # add final variable
            if i == len(self.topology)-1 and self.topology[i][0] not in temp:
                temp.append(self.topology[i][0])
            # deep copy
            out.append(temp[:]) 
        return out