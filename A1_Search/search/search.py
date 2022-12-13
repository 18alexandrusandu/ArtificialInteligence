# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from datetime import datetime

import util
from graphicsUtils import keys_waiting
from graphicsUtils import keys_pressed

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


from util import *


def depthFirstSearch(problem):
    print("dfs")
    frontier = Stack()
    extended = []
    frontier.push((problem.getStartState(), 0, 0, 0, 0))
    while not frontier.isEmpty():
        node = frontier.pop()
        extended.append(node)
        if problem.isGoalState(node[0]):
            actions = Queue()
            parent = node[2]
            actions.push(node[1])
            while not parent == 0:
                for n in extended:
                    if n[0] == parent:
                        actions.push(n[1])
                        parent = n[2]
                        break
            return actions.list[1:]
        vecini = problem.getSuccessors(node[0])
        for v in vecini:
            bool = False
            for e in extended:
                if e[0] == v[0]:
                    bool = True
            if bool == False:
                frontier.push((v[0], v[1], node[0], v[2]))


"""
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """


def breadthFirstSearch(problem):
    print("bfs")
    frontier = Queue()
    extended = []

    frontier.push((problem.getStartState(), 0, 0, 0, 0))

    while not frontier.isEmpty():
        node = frontier.pop()
        extended.append(node)
        if problem.isGoalState(node[0]):
            actions = Queue()
            parent = node[2]
            actions.push(node[1])
            while not parent == 0:
                for n in extended:
                    if n[0] == parent:
                        actions.push(n[1])
                        parent = n[2]
                        break
            print("expended during bfs",len(extended))
            print("solution length during bfs", len(actions.list[1:]))
            return actions.list[1:]
        vecini = problem.getSuccessors(node[0])
        for v in vecini:
            bool = False
            for e in extended:
                if e[0] == v[0]:
                    bool = True
            if bool == False:
                frontier.push((v[0], v[1], node[0], v[2]))


def uniformCostSearch(problem):
    print("ucs")
    frontier = PriorityQueue()
    extended = []
    frontier.push((problem.getStartState(), 0, 0, 0, 0), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        extended.append(node)

        if problem.isGoalState(node[0]):
            actions = Queue()
            parent = node[2]
            actions.push(node[1])
            while not parent == 0:
                for n in extended:
                    if n[0] == parent:
                        actions.push(n[1])
                        parent = n[2]
                        break
            return actions.list[1:]
        vecini = problem.getSuccessors(node[0])
        for v in vecini:
            bool = False
            for e in extended:
                if e[0] == v[0]:
                    bool = True
            if bool == False:
                costTotal = node[3] + v[2]
                frontier.push((v[0], v[1], node[0], costTotal), costTotal)

    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5






from game import Directions



def SightHeuristic(position,problem):
    x,y=position
    noWallAhead=True
    noGhostAhead=True
    problem.getWalls();




    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    print("astar")
    frontier = PriorityQueue()
    extended = []
    frontier.push((problem.getStartState(), 0, 0, 0), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        extended.append(node)
        if problem.isGoalState(node[0]):
            return build_path(extended,problem.visitedCorners,problem.getStartState())
        vecini = problem.getSuccessors(node[0])
        for v in vecini:
            bool = False
            for e in extended:
                 if  e[0] == v[0]:
                    bool = True
            if bool == False:
                costTotal = node[3] + v[2]
                heuristicCost = heuristic(v[0], problem) + costTotal
                frontier.push((v[0], v[1], node[0], costTotal), heuristicCost)




def build_path(extended,visitedCorners,start_point):
    paths = []
    actions = Queue()
    parent=(0,0,0,0)
    for vc in visitedCorners:
        path = Stack()

        for n in extended:
         if(n[0]==vc):
           print("n0",n)
           path.push(n)
           parent = n[0]
           break


        print("extended",extended)

        while not parent == 0:
            print("parent",parent)
            for n in extended:
                if n[0] == parent:
                    path.push(n)
                    parent = n[2]
                    break

        paths.append(path.list[1:])
    print("visited corners in order are:", visitedCorners)
    print("paths are:")
    for path1 in paths:
        print("path:", path1)
    noduri_legatura = [0,0,0,0,0,0,0]
    search_intersections=[1,2,3,4,5,6]
    for i in paths[0]:
        for j in paths[1]:
            for k in paths[2]:
                for l in paths[3]:
                    for m in range(len(search_intersections)):
                         if i[0] == j[0] and search_intersections[m]==1:
                             search_intersections[m]=0
                             noduri_legatura[1]=i

                         if i[0] == k[0] and search_intersections[m] == 4:
                             search_intersections[m] = 0
                             noduri_legatura[4]=j
                         if i[0] == l[0] and search_intersections[m] == 5:
                             search_intersections[m] = 0
                             noduri_legatura[5]=l
                         if j[0] == k[0] and search_intersections[m] == 2:
                             search_intersections[m] = 0
                             noduri_legatura[2]=k
                         if j[0] == l[0] and search_intersections[m] == 6:
                             search_intersections[m] = 0
                             noduri_legatura[6]=j
                         if l[0] == k[0] and search_intersections[m] == 3:
                             search_intersections[m] = 0
                             noduri_legatura[3]=l
    print("noduri de legatura in arbore sunt:", noduri_legatura)
    destination = start_point
    for i in range(0,4):
     print("i=",i)
     current_possition = paths[i][0]

     #reverse a path:

     help_stack =Stack()
     help_stack2=Queue()
     print("starting point", current_possition )
     for n in paths[i]:
          print("destination to get to",destination)
          if n[0]==destination:

              print("destination",destination)
              help_stack=Stack()
              nod_to_go_back_to=0
              current_possiton=paths[i][0]
              if i==3:
                nod_to_go_back_to = noduri_legatura[i -1][0]
              else:
                nod_to_go_back_to = noduri_legatura[i +1 ][0]
              print("go  back to",nod_to_go_back_to)
              print("current", current_possition )
              destination= nod_to_go_back_to
         #     #you reached a point from where you will jump to an intersection so go back to that point
              while  not  (current_possition[0]==nod_to_go_back_to )and  not current_possition[2]==0:


                 print("backtracking",current_possition)
                #reverse the action made to get to a corner
                 if (current_possition[1] == 'North'):
                    help_stack.push("South")
                 if (current_possition[1]  == 'South'):
                    help_stack.push("North")
                 if (current_possition[1] == 'West'):
                    help_stack.push("East")
                 if (current_possition[1] == 'East'):
                    help_stack.push('West')
                #go back to your parent
                 for j in extended:
                    if j[0]==current_possition[2]:
                        current_possition=j
                        break
              print(" finished backtracking")


              break
          else:

               if n[1]!=0:
                 print("n not path",n)
                 help_stack2.push(n[1])


     actions.list=actions.list+help_stack2.list+help_stack.list
     print("actions after a path",actions.list)

    print("actions",actions.list)
    return actions.list










#for corners problem
def weightedAstarSearch(problem, heuristic=nullHeuristic, weightE=2, weightC=1):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    print("Wastar")
    frontier = PriorityQueue()
    extended = []
    actions = Queue()
    frontier.push((problem.getStartState(), 0, 0, 0), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        extended.append(node)
        print("number of corners not riched",len(problem.remainingCorners))
        if problem.isGoalState(node[0]):
            print("goal riched")

            return build_path(extended,problem.visitedCorners,problem.getStartState())
        vecini = problem.getSuccessors(node[0])
        print("vecini",vecini)
        for v in vecini:
               bool = False
               for e in extended:
                  if e[0] == v[0]:
                       bool = True
               if bool == False:
                print("can add mmore")
                costTotal = node[3] + v[2]
                heuristicCost = weightE * heuristic(v[0], problem) + weightC * costTotal
                frontier.push((v[0], v[1], node[0], costTotal), heuristicCost)
    print("no new nodes")
    return []
def DinamicWeightedAstarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    print("remainingCorners",problem.remainingCorners)
    print("DWastar")
    frontier = PriorityQueue()
    extended = []
    frontier.push((problem.getStartState(), 0, 0, 0), 0)
    depth=0;
    random.seed(datetime.now())
    epsilon=random.random();
   # len(breadthFirstSearch(problem))
    N=60
    extended = []
    problem.remainingCorners=[problem.corners[0],problem.corners[1],problem.corners[2],problem.corners[3]]
    pause();
    while not frontier.isEmpty():
        depth=depth+1;
        weightE=1+epsilon-epsilon*depth/N;
        print("weightE",weightE);
        node = frontier.pop()
        extended.append(node)
        if problem.isGoalState(node[0]):
          print("got to goal")
          print("extended",extended)
          pause();
          return build_path(extended,problem.visitedCorners,problem.getStartState())

        vecini = problem.getSuccessors(node[0])
        for v in vecini:
            bool = False
            for e in extended:
                if e[0] == v[0]:
                    bool = True
            if bool == False:
                costTotal = node[3] + v[2]
                heuristicCost = weightE * heuristic(v[0], problem) + costTotal
                frontier.push((v[0], v[1], node[0], costTotal), heuristicCost)


def CostOrientedWeightAStar(problem, heuristic=nullHeuristic, weightE=2, weightC=1):
     return weightedAstarSearch(problem, heuristic, 1, 2)


def HeuristicOrientedWeightAStar(problem, heuristic=nullHeuristic, weightE=2, weightC=1):
    return weightedAstarSearch(problem, heuristic, 2, 1)


def greedyWeightAStar(problem, heuristic=nullHeuristic, weightE=2, weightC=1):
    return weightedAstarSearch(problem, heuristic ,1,0)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
wastar = weightedAstarSearch

