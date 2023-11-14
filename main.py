import random
import copy
from matplotlib import pylab

class CityGrid:
    
    def __init__(self, N, M, coverage):
        self.N = N 
        self.M = M  
        self.gridArray = [[random.choices([ '0  ' , 'B  '], weights=[100 - coverage, coverage])[0] for j in range(self.M)] for i in range(self.N)]
        self.towerCounter = 0
        self.R = 0
        self.coverageRadius = 0
        self.linkRadius = 0


    def BuildTowers(self, R):
        self.R = R
        self.linkRadius = self.R * 4 + 3
        self.coverageRadius = self.R * 2 + 1
        j = 0 # 
        k = 0 # coords of uncovered point
        while (j < self.N and k < self.M):
            if(self.gridArray[j][k] == '0  '):
                iterationAmmount = 0 
                directionUp = True # up or left
                columnRadius = R
                rowRadius = R
                if(j + R < self.N):
                    iterationAmmount = 0 # counts the decrease in coulumns from uncovered point to tower 
                else:
                    rowRadius = self.N - R - j - 1
                    iterationAmmount = 0 # counts ladder iterrations
                while(True):#columnRadius >= 0 and rowRadius >= 0
                    if(j + rowRadius < self.N and k + columnRadius < self.M):
                        if (self.gridArray[j + rowRadius][k + columnRadius] == '0  ' or self.gridArray[j + rowRadius][k + columnRadius] == 'C  '):
                            self.towerCounter += 1
                            if (self.towerCounter < 10):
                                self.gridArray[j + rowRadius][k + columnRadius] = 'T' + str(self.towerCounter) + ' '
                            else:
                                self.gridArray[j + rowRadius][k + columnRadius] = 'T' + str(self.towerCounter)
                            self.ShowTowerCoverage(j + rowRadius, k + columnRadius, R)
                            break  

                    if(j + R < self.N):
                        if(directionUp):
                            if rowRadius > 0:
                                rowRadius -= 1
                            else:
                                rowRadius = R - iterationAmmount
                                directionUp = False
                        else:
                            if columnRadius > 0:
                                columnRadius -= 1
                            else:
                                iterationAmmount += 1
                                columnRadius = R - iterationAmmount
                                directionUp = True
                    else:
                        if((columnRadius - 1 <= 0 or rowRadius <= self.N - R - j - 1) and not(columnRadius == 1 and rowRadius == 1)):
                            iterationAmmount += 1
                            columnRadius = R
                            rowRadius = self.N - R - j - 1 + iterationAmmount
                        else:
                            columnRadius -= 1
                            rowRadius -= 1

            if(j + 1 < self.N):
                j += 1
            else:
                j = 0
                k += 1

    def ShowTowerCoverage(self, rowTower, columnTower, R):
        for i in range(2 * R + 1):
            for j in range(2 * R + 1):
                if(rowTower - R + i < self.N and columnTower - R + j < self.M and (self.gridArray[rowTower - R + i][columnTower - R + j] == '0  ')):
                            self.gridArray[rowTower - R + i][columnTower - R + j] = 'C  '

    def PathfinderBetweenTowers(self, startTower, finishTower): # towers can links if radiuses are connected
        if(startTower == finishTower):
            return 'T' + str(startTower)
        
        gridCopy = copy.deepcopy(self.gridArray)
        isCoordsFounded = False
        for i in range(self.N):
            for j in range(self.M):
                if(gridCopy[i][j].replace(' ', '') == 'T' + str(startTower)):
                    gridCopy[i][j] = '0'
                    isCoordsFounded = True
                    break
            if(isCoordsFounded):
                break
        
        pathCurrentLength = 0
        finishFounded = False
        isFinishExist = True
        
        while(not finishFounded):
            isCoordsFounded = False
            towerCoords = [-1, -1]
            for i in range(self.N):
                for j in range(self.M):
                    if(gridCopy[i][j].replace(' ', '') == str(pathCurrentLength)):
                        gridCopy[i][j] = str(pathCurrentLength) + 'Ch'
                        towerCoords = [i,j]
                        isCoordsFounded = True
                        isFinishExist = True
                        break
                if(isCoordsFounded):
                    break
            
            if(not isCoordsFounded):
                if(not isFinishExist):   
                    print()
                    for i in gridCopy:
                        print(i)  
                    return 'No path'
                isFinishExist = False
                pathCurrentLength += 1
            else:
                for i in range(self.linkRadius):
                    for j in range(self.linkRadius):
                        if 0 <= towerCoords[0] - self.coverageRadius + i < self.N and 0 <= towerCoords[1] - self.coverageRadius  + j < self.M:  
                            if 'T' in gridCopy[towerCoords[0] - self.coverageRadius + i][towerCoords[1] - self.coverageRadius + j]:
                                if(gridCopy[towerCoords[0] - self.coverageRadius + i][towerCoords[1] - self.coverageRadius + j].replace(' ', '') == 'T' + str(finishTower)):
                                    finishFounded = True
                                    gridCopy[towerCoords[0] - self.coverageRadius + i][towerCoords[1] - self.coverageRadius + j] = str(pathCurrentLength + 1) + 'F'
                                else:
                                    gridCopy[towerCoords[0] - self.coverageRadius + i][towerCoords[1] - self.coverageRadius + j] = str(pathCurrentLength + 1)

        path = ''
        curPathPart = 0
        lastcoord = []
        for i in range(self.N):
            for j in range(self.M):
                if 'F' in gridCopy[i][j]:
                    curPathPart = int(gridCopy[i][j].replace('F', ''))
                    lastcoord = [i,j]
                    path = str(self.gridArray[i][j]) + ' ' + path
                    curPathPart -= 1

        while(curPathPart >= 0):
            for i in range(self.linkRadius):
                for j in range(self.linkRadius):
                    if 0 <= lastcoord[0] - self.coverageRadius + i < self.N and 0 <= lastcoord[1] - self.coverageRadius  + j < self.M: 
                        if gridCopy[lastcoord[0] - self.coverageRadius + i][lastcoord[1] - self.coverageRadius + j] == str(curPathPart) + 'Ch':
                            curPathPart = int(gridCopy[lastcoord[0] - self.coverageRadius + i][lastcoord[1] - self.coverageRadius + j].replace('Ch', ''))
                            path = str(self.gridArray[lastcoord[0] - self.coverageRadius + i][lastcoord[1] - self.coverageRadius + j]) + ' ' + path
                            lastcoord = [lastcoord[0] - self.coverageRadius + i,lastcoord[1] - self.coverageRadius + j]
                            curPathPart -= 1

        for i in gridCopy:
            print(i)                   

        print()

        for i in a.gridArray:
            print(i)                   

        return(path)            
     
    def ShowWithMathlib(self):
        print('plot')

        # pylab.plot(range(5), range(5))
        pylab.figure(figsize=(15,10))
        pylab.xlabel('N')
        pylab.ylabel('M')
        pylab.title('City Grid')
        pylab.grid(True)
        pylab.grid(axis='both', linewidth = 1)
        pylab.style.use('fivethirtyeight')
        pylab.tight_layout()
        # pylab.plot([1],[1] , marker = 'o')
        
        pylab.plot([1],[1] , 'yo', label='Coverage')
        pylab.plot([1],[1] , 'bd', label='Tower')
        pylab.plot([1],[1] , 'rx', label='Obstacle')

        for i in range(self.N):
            for j in range(self.M): 
                if 'C' in a.gridArray[i][j]:
                    pylab.plot([i],[j] , 'yo')
                elif 'T' in a.gridArray[i][j]:
                    pylab.plot([i],[j] , 'bd')
                elif 'B' in a.gridArray[i][j]:
                    pylab.plot([i],[j] , 'rx')
        
        pylab.legend()
        xAr = []
        yAr = []


        startTower = random.randint(1, a.towerCounter)
        finishTower = random.randint(1, a.towerCounter)
        if (a.towerCounter > 2):    
            while(startTower == finishTower):
                finishTower = random.randint(1, a.towerCounter)
        print(startTower)
        print(finishTower)
        answ = self.PathfinderBetweenTowers(startTower,finishTower)
        print(answ)
        for i in answ.split(' '):
            for n in range(self.N):
                for k in range(self.M):
                    if (len(i) < 3 and i + ' ' == a.gridArray[n][k]) or (len(i) >= 3 and i == a.gridArray[n][k]):          
                            xAr.append(n)
                            yAr.append(k)

        pylab.plot(xAr,yAr, 'c--')
        # 0 coverage
        # d tower
        # x obst
        
        pylab.show()

        




N = random.randint(15, 70)
print(N)
M = random.randint(15, 70)
print(M)
while(N == M):
    M = random.randint(3, 20)
coverage = random.randint(30, 40)
print(coverage)

a = CityGrid(N,M,coverage)

# for i in a.gridArray:
#     print(i)

# print()

a.BuildTowers(random.randint(2, 2))
# for i in a.gridArray:
#     print(i)

a.ShowWithMathlib()

input()