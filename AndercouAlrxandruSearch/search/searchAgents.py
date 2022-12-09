# searchAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from math import sqrt
from random import random

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search


class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError, fn + ' is not a search function in search.py.'
        func = getattr(search, fn)
        if 'heuristic' not in func.func_code.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError, heuristic + ' is not a function in searchAgents.py or search.py.'
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):

        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem+ self.actions)\
        print("searchFunction",self.searchFunction)
        self.actions  = self.searchFunction(problem) # Find a path


        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState,costFn = lambda x: 1):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.startingGameState=startingGameState
        self.walls = startingGameState.getWalls()
        self.costFn=costFn
        self.startState = startingGameState.getPacmanPosition()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))

        self.remainingCorners=[(1,1), (1,top), (right, 1), (right, top)]
        self.visitedCorners=[]
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"

        return self.startState;

    def isGoalState(self, state):
        x,y =state
        for i  in range(len(self.remainingCorners)):
           x1,y1=self.remainingCorners[i]
           if(x==x1 and y==y1):
                self.visitedCorners.append(self.remainingCorners[i])
                self.remainingCorners.remove(self.remainingCorners[i])
                i=i-1
                break

        isGoal=len(self.remainingCorners) == 0
        if isGoal:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors


    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999

        return len(actions)


def cornersHeuristic1(state, problem):
    corners = problem.remainingCorners
    return len(corners)

def cornersHeuristic2(state, problem):
    # These are the corner coordinates
    x,y= state
    corners=problem.remainingCorners
    furthestcornerIndex=0
    biggestDistance= -1
    for index in xrange(0,len(corners)):
       xg,yg= corners[index]
       dist=abs(x-xg)+abs(x-xg)
       if dist>biggestDistance:
           biggestDistance =dist
           furthestcornerIndex=index
    xg, yg = corners[furthestcornerIndex]

    return abs(x-xg)*abs(y-yg)





def cornersHeuristic3(state, problem):
    corners = problem.remainingCorners
    # These are the corner coordinates
    x,y= state
    bigestDistanceBetweenCorners=0;
    closestCorner=999999;
    print("remaining corners",len(corners))
    for i in range(len(corners)):
         xc, yc = corners[i]
         dist_corners=mazeDistance((x,y),(xc,yc),problem.startingGameState)

         if(dist_corners<closestCorner):
             closestCorner=dist_corners

         for j in (i+1,len(corners)-1):
            if j<len(corners):
              xc2,yc2=corners[j]
              dist=mazeDistance((xc,yc),(xc2,yc2),problem.startingGameState)
              if dist >  bigestDistanceBetweenCorners:
                 bigestDistanceBetweenCorners=dist

    return closestCorner+bigestDistanceBetweenCorners


def cornersHeuristic4(state, problem):
    corners = problem.remainingCorners
    # These are the corner coordinates
    x,y= state
    averageDistanceBetweenCorners=0;
    closestCorner=999999;

    for i in range(len(corners)):
         xc, yc = corners[i]
         dist_corners=mazeDistance((x,y),(xc,yc),problem.startingGameState)
         if(dist_corners<closestCorner):
             closestCorner=dist_corners

         for j in(i+1,len(corners)):
          if j < len(corners):
            xc2,yc2=corners[j]
            dist=mazeDistance((x,y),(xc,yc),problem.startingGameState)
            averageDistanceBetweenCorners +=dist

    return closestCorner+averageDistanceBetweenCorners/len(corners)




def cornersHeuristic5(state, problem):
    corners = problem.remainingCorners
    # These are the corner coordinates
    x,y= state
    averageDistanceBetweenCorners=0;
    closestCorner=999999;

    for i in range(len(corners)):
         xc, yc = corners[i]
         #=abs(x-xc)+abs(y-yc)
         dist_corners=abs(x-xc)+abs(y-yc)
         if(dist_corners<closestCorner):
             closestCorner=dist_corners

         for j in(i+1,len(corners)):
          if j < len(corners):
            xc2,yc2=corners[j]
            dist=abs(xc-xc2)+abs(yc-yc2)
            averageDistanceBetweenCorners +=dist

    return closestCorner+averageDistanceBetweenCorners/len(corners)





class AStarCornersAgent(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic1)
        self.searchType = CornersProblem

class AStarCornersAgentWeightedCO(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.CostOrientedWeightAStar(prob,cornersHeuristic1)
        self.searchType = CornersProblem

class AStarCornersAgentWeightedHO(SearchAgent):
     def __init__(self):
        self.searchFunction = lambda prob: search.HeuristicOrientedWeightAStar(prob,cornersHeuristic1)
        self.searchType = CornersProblem


class GreedyCornersAgentHeuristic(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.greedyWeightAStar(prob, cornersHeuristic1)
        self.searchType = CornersProblem


class DinamicCornersAgentHeuristic(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.DinamicWeightedAstarSearch(prob, cornersHeuristic1)
        self.searchType = CornersProblem



class AStarCornersAgenth2(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic2)
        self.searchType = CornersProblem

class AStarCornersAgentWeightedCO2(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.CostOrientedWeightAStar(prob,cornersHeuristic2)
        self.searchType = CornersProblem


class AStarCornersAgentWeightedHO2(SearchAgent):
     def __init__(self):
        self.searchFunction = lambda prob: search.HeuristicOrientedWeightAStar(prob,cornersHeuristic2)
        self.searchType = CornersProblem


class GreedyCornersAgentHeuristic2(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.greedyWeightAStar(prob, cornersHeuristic2)
        self.searchType = CornersProblem

class DinamicCornersAgentHeuristic2(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.DinamicWeightedAstarSearch(prob, cornersHeuristic2)
        self.searchType = CornersProblem


class AStarCornersAgenth3(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic3)
        self.searchType = CornersProblem

class AStarCornersAgentWeightedCO3(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.CostOrientedWeightAStar(prob,cornersHeuristic3)
        self.searchType = CornersProblem


class AStarCornersAgentWeightedHO3(SearchAgent):
     def __init__(self):
        self.searchFunction = lambda prob: search.HeuristicOrientedWeightAStar(prob,cornersHeuristic3)
        self.searchType = CornersProblem


class GreedyCornersAgentHeuristic3(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.greedyWeightAStar(prob, cornersHeuristic3)
        self.searchType = CornersProblem

class DinamicCornersAgentHeuristic3(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.DinamicWeightedAstarSearch(prob, cornersHeuristic3)
        self.searchType = CornersProblem


class AStarCornersAgenth4(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic4)
        self.searchType = CornersProblem


class AStarCornersAgentWeightedCO4(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.CostOrientedWeightAStar(prob,cornersHeuristic4)
        self.searchType = CornersProblem


class AStarCornersAgentWeightedHO4(SearchAgent):
     def __init__(self):
        self.searchFunction = lambda prob: search.HeuristicOrientedWeightAStar(prob,cornersHeuristic4)
        self.searchType = CornersProblem


class GreedyCornersAgentHeuristic4(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.greedyWeightAStar(prob, cornersHeuristic4)
        self.searchType = CornersProblem

class DinamicCornersAgentHeuristic4(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.DinamicWeightedAstarSearch(prob, cornersHeuristic4)
        self.searchType = CornersProblem


class AStarCornersAgenth5(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic5)
        self.searchType = CornersProblem


class AStarCornersAgentWeightedCO5(SearchAgent):

    def __init__(self):
        self.searchFunction = lambda prob: search.CostOrientedWeightAStar(prob, cornersHeuristic5)
        self.searchType = CornersProblem


class AStarCornersAgentWeightedHO5(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.HeuristicOrientedWeightAStar(prob, cornersHeuristic5)
        self.searchType = CornersProblem


class GreedyCornersAgentHeuristic5(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.greedyWeightAStar(prob, cornersHeuristic5)
        self.searchType = CornersProblem


class DinamicCornersAgentHeuristic5(SearchAgent):
    def __init__(self):
        self.searchFunction = lambda prob: search.DinamicWeightedAstarSearch(prob, cornersHeuristic5)
        self.searchType = CornersProblem


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic1)
        self.searchType = FoodSearchProblem

def foodHeuristic1(state, problem):
    position, foodGrid = state
    howMuchFood=0
    nrfood=0
    positions=foodGrid.asList()
    for pos in positions:
        x,y=pos
        if  foodGrid[x][y]==True:
            nrfood=nrfood+1
    "*** YOUR CODE HERE ***"
    return nrfood

def foodHeuristic2(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    xp,yp=position
    howMuchFood=0
    nrfood=0
    positions=foodGrid.asList()
    smallestDisatance=999999
    for pos in positions:
        x,y=pos
        if  foodGrid[x][y]==True:
            nrfood=nrfood+1
            dist=(x-xp)*(x-xp)+(y-yp)*(y-yp)
            if dist<smallestDisatance:
                smallestDisatance=dist

    "*** YOUR CODE HERE ***"
    return nrfood*smallestDisatance




class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print 'Path found with cost %d.' % len(self.actions)

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AnyFoodSearchProblem(PositionSearchProblem):

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        PositionSearchProblem.__init__(self, gameState)
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
