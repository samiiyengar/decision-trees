import sys
import copy


class node:
    '''
    This class is for book-keeping each state in the MDP.

    self.util is the utility of this state
    self.reward is R(s), the reward of getting to this state
    self.isWall is a flag that indicates whether this cell is occupied by wall
    self.isTerminal is a flag that indicates whether this state is a terminal state.

    '''
    def __init__(self, util = 0, reward=-0.04, isWall=False, isTerminal=False):
        self.util = util
        self.reward = reward
        self.isWall = isWall
        self.isTerminal = isTerminal

class grid:
    '''
    This class represents our MDP problem. It consists of

    - Description of the environment
    - Method to print the grid
    - Method to do Value Iteration (you need to implement)

    '''

    '''DO NOT EDIT THIS'''
    def __init__(self, gridfile):
        '''
        This init function helps you read and parse the environment file.
        And it maintains the below data members:

        self.gamma : discount factor
        self.living_cost : "cost of living", a negative reward
        self.mprobs : transition probabilities
        self.grid : a rectangle (defined by nrows-by-ncols) that represents
                    the environment
        '''
        line = open(gridfile, 'r').readlines()
        self.gamma = float(line[0])
        self.living_cost = float(line[1])
        mprobs = line[2].split()
        self.mprobs = [float(n) for n in mprobs]
        self.grid = []
        for row in line[3:]:
            gridrow = []
            splitrow = row.split()
            if len(splitrow) == 0:
                continue
            for ch in row.split():
                if ch == '*':
                    gridrow.append(node(reward=self.living_cost))
                elif ch == 'x':
                    gridrow.append(node(isWall=True))
                else:
                    try:
                        utility = float(ch)
                        gridrow.append(node(util=utility, isTerminal=True))
                    except ValueError:
                        print ("Bad grid value")
                        sys.exit()
            self.grid.append(gridrow)
        self.nrows = len(self.grid)
        assert(self.nrows > 0)
        self.ncols = len(self.grid[0])
        assert(self.ncols > 0)

    def printGrid(self):
        '''
        Print the grid
        '''
        printstr = ''
        for row in self.grid:
            for c in row:
                if not c.isWall:
                    printstr += str(round(c.util, 3)) + ' '
                else:
                    printstr += 'x '
            printstr += '\n'
        print (printstr)

    def is_coord_open(self, i, j):
        '''
        Checks if there is a grid space at (i,j), and whether or not there is a wall there
        Returns True if there is a free grid space
        Returns False otherwise
        '''
        if i >= 0 and j < self.ncols and i < self.nrows and j >= 0 and not self.grid[i][j].isWall:
            return True
        else:
            return False

    '''
        TODO:
    '''
    def doValueIteration(self, epsilon=0.00001):
        '''
        This function modifies the utilities of each cell in the grid.
        
        Input:
            epsilon : the maximum error allowed in the utility of any state
            self: this MDP problem
        
        Output:
            No need to return anything. You just need to modify the utility for
            each cell (state) in self.grid.
        '''
        delta = 1
        convergence = min((1-self.gamma)/self.gamma,1)
        if convergence == 0:
            convergence = 1
        niters = 0
        while delta >= epsilon*convergence or niters < 1000:
            delta = 0
            newgrid = copy.deepcopy(self.grid)
            for i in range(self.nrows):
                for j in range(self.ncols):
                    cur = self.grid[i][j]
                    if cur.isWall or cur.isTerminal:
                        continue
                    # value iteration
                    best_ev = self.grid[i][j].util
                    ev1 = float('-inf')
                    if self.is_coord_open(i+1, j):
                        ev1 = self.mprobs[0] * newgrid[i+1][j].util
                        if (self.is_coord_open(i, j+1)):
                            ev1 += self.mprobs[1] * newgrid[i][j+1].util
                        else:
                            ev1 += self.mprobs[1] * newgrid[i][j].util
                        if (self.is_coord_open(i-1, j)):
                            ev1 += self.mprobs[2] * newgrid[i-1][j].util
                        else:
                            ev1 += self.mprobs[2] * newgrid[i][j].util
                        if (self.is_coord_open(i, j-1)):
                            ev1 += self.mprobs[3] * newgrid[i][j-1].util
                        else:
                            ev1 += self.mprobs[3] * newgrid[i][j].util
                    else:
                        ev1 = self.mprobs[0] * newgrid[i][j].util
                        
                    ev2 = float('-inf')
                    if self.is_coord_open(i, j+1):
                        ev2 = self.mprobs[0] * newgrid[i][j+1].util
                        if (self.is_coord_open(i+1, j)):
                            ev2 += self.mprobs[1] * newgrid[i+1][j].util
                        else:
                            ev2 += self.mprobs[1] * newgrid[i][j].util
                        if (self.is_coord_open(i, j-1)):
                            ev2 += self.mprobs[2] * newgrid[i][j-1].util
                        else:
                            ev2 += self.mprobs[2] * newgrid[i][j].util
                        if (self.is_coord_open(i-1, j)):
                            ev2 += self.mprobs[3] * newgrid[i][j-1].util
                        else:
                            ev2 += self.mprobs[3] * newgrid[i][j].util
                    else:
                        ev2 = self.mprobs[0] * newgrid[i][j].util
                        
                    ev3 = float('-inf')
                    if self.is_coord_open(i-1, j):
                        ev3 = self.mprobs[0] * newgrid[i-1][j].util
                        if (self.is_coord_open(i, j+1)):
                            ev3 += self.mprobs[1] * newgrid[i][j+1].util
                        else:
                            ev3 += self.mprobs[1] * newgrid[i][j].util
                        if (self.is_coord_open(i+1, j)):
                            ev3 += self.mprobs[2] * newgrid[i+1][j].util
                        else:
                            ev3 += self.mprobs[2] * newgrid[i][j].util
                        if (self.is_coord_open(i, j-1)):
                            ev3 += self.mprobs[3] * newgrid[i][j-1].util
                        else:
                            ev3 += self.mprobs[3] * newgrid[i][j].util
                    else:
                        ev3 = self.mprobs[0] * newgrid[i][j].util
                        
                    ev4 = float('-inf')
                    if self.is_coord_open(i, j-1):
                        ev4 = self.mprobs[0] * newgrid[i][j-1].util
                        if (self.is_coord_open(i+1, j)):
                            ev4 += self.mprobs[1] * newgrid[i+1][j].util
                        else:
                            ev4 += self.mprobs[1] * newgrid[i][j].util
                        if (self.is_coord_open(i, j+1)):
                            ev4 += self.mprobs[2] * newgrid[i][j+1].util
                        else:
                            ev4 += self.mprobs[2] * newgrid[i][j].util
                        if (self.is_coord_open(i-1, j)):
                            ev4 += self.mprobs[3] * newgrid[i-1][j].util
                        else:
                            ev4 += self.mprobs[3] * newgrid[i][j].util
                    else:
                        ev4 = self.mprobs[0] * newgrid[i][j].util
                        
                    best_ev = max(ev1, ev2, ev3, ev4, best_ev)
                    self.grid[i][j].util = cur.reward + self.gamma * best_ev
                    if abs(self.grid[i][j].util - newgrid[i][j].util) > delta:
                        delta = abs(self.grid[i][j].util - newgrid[i][j].util)
            niters += 1
        return newgrid
            
if __name__=='__main__':
    assert(len(sys.argv)>1)
    g = grid(sys.argv[1])
    g.doValueIteration()
    g.printGrid()

