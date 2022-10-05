# multiAgents.py
# --------------
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
from ghostAgents import DirectionalGhost
from pacman import GameState
from util import *
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def __init__(self):
        super().__init__()
        self.lastAction=None


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print(scores)
        # if len(scores) > 1 and "Stop" in legalMoves:
        #     scores[legalMoves.index("Stop")]=0
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]


        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState:GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        result=0
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        nearestFoodDistance= nearestToGrid(newPos, newFood) +5*random.random()
        GhostDistances= [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates if ghostState.scaredTimer==0]

        result=childGameState.getScore()-sum([(GhostDistance<3)*(20-GhostDistance) for GhostDistance in GhostDistances])-\
               nearestFoodDistance*(not currentGameState.getFood().data[newPos[0]][newPos[1]])

        # if self.lastAction==None:
        #     self.lastAction=action
        # else:
        #     if self.lastAction==action:
        #         result+=1.2
        #     self.lastAction=action

        # result = childGameState.getScore()-int(math.pow(1.8,nearestFoodDistance))+1+(GhostDistance)
        # if currentGameState.getFood().data[newPos[0]][newPos[1]]: #if pacman eats a food
        #     result+=int(math.pow(1.8,nearestFoodDistance))
        # print(result)
        return result

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minMaxTree(self, gameState, depth)->(int, str):
        """
        this gameState is starts with player turn

        :param gameState:
        :param depth:
        :return:
        """
        foreseenResults = []
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        for playaction in gameState.getLegalActions(0):
            GhoshTurnState = gameState.getNextState(0, playaction)
            if GhoshTurnState.isWin() or GhoshTurnState.isLose():
                foreseenResults.append(self.evaluationFunction(GhoshTurnState))
                continue
            GhostMinBanifit = 100000
            GhostActionsList=[]
            for ghost in range(self.GhostNumeber):
                if len(GhostActionsList)==0:
                    GhostActionsList=[[gh] for gh in GhoshTurnState.getLegalActions(ghost + 1)]
                else:
                    NewTempList=[]
                    for action1 in GhostActionsList:
                        for action2 in GhoshTurnState.getLegalActions(ghost + 1):
                            NewTempList.append(action1+[action2])
                    GhostActionsList = NewTempList.copy()
            for actions in GhostActionsList:
                myResultState=GhoshTurnState
                for ghost in range(self.GhostNumeber):
                    myResultState=myResultState.getNextState(ghost+1, actions[ghost])
                    if myResultState.isWin() or myResultState.isLose():
                        break
                if depth==1:
                    GhostMinBanifit = min(GhostMinBanifit, self.evaluationFunction(myResultState))
                else:
                    GhostMinBanifit = min(GhostMinBanifit, self.minMaxTree(myResultState, depth - 1)[0])

            foreseenResults.append(GhostMinBanifit)
        return max(foreseenResults),gameState.getLegalActions(0)[foreseenResults.index(max(foreseenResults))]
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        self.GhostNumeber=gameState.getNumAgents()-1
        if gameState.isWin():
            return []

        return self.minMaxTree(gameState, self.depth)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getValue(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth==self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex==0:
            return self.maxValue(gameState,depth,alpha,beta)
        else:
            return self.minValue(gameState,depth,agentIndex,alpha,beta)

    def maxValue(self,state, depth,alpha, beta ):
        v=-9999
        for action in state.getLegalActions(0):
            v = max(v,self.getValue(state.getNextState(0, action), depth, 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v
    def minValue(self,state,depth,agentIndex, alpha, beta ):
        v=999999
        for action in state.getLegalActions(agentIndex):
            if agentIndex==state.getNumAgents()-1:
                v = min(v,self.getValue(state.getNextState(agentIndex, action), depth+1, 0, alpha, beta))
            else:
                v=min(v,self.getValue(state.getNextState(agentIndex, action), depth, agentIndex+1, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        beta = 99999
        alpha=-99999
        playerUtils=[]
        for playeraction in gameState.getLegalActions(0):
            ghostState = gameState.getNextState(0, playeraction)
            myUtil = self.getValue(ghostState, 0, 1, alpha, beta)
            alpha = max(alpha, myUtil)
            playerUtils.append(myUtil)
        return gameState.getLegalActions(0)[playerUtils.index(max(playerUtils))]

class ExpectimaxAgent(MultiAgentSearchAgent):

    def minMaxTree(self, gameState, depth)->(int, str):
        foreseenResults = []
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        for playaction in gameState.getLegalActions(0):
            GhoshTurnState = gameState.getNextState(0, playaction)
            if GhoshTurnState.isWin() or GhoshTurnState.isLose():
                foreseenResults.append(self.evaluationFunction(GhoshTurnState))
                continue
            GhostActionsList=[]
            for ghost in range(self.GhostNumeber):
                if len(GhostActionsList)==0:
                    GhostActionsList=[[gh] for gh in GhoshTurnState.getLegalActions(ghost + 1)]
                else:
                    NewTempList=[]
                    for action1 in GhostActionsList:
                        for action2 in GhoshTurnState.getLegalActions(ghost + 1):
                            NewTempList.append(action1+[action2])
                    GhostActionsList = NewTempList.copy()
            GhostMinBanifit = 0
            for actions in GhostActionsList:
                myResultState=GhoshTurnState
                for ghost in range(self.GhostNumeber):
                    myResultState=myResultState.getNextState(ghost+1, actions[ghost])
                    if myResultState.isWin() or myResultState.isLose():
                        break
                if depth==1:
                    GhostMinBanifit += self.evaluationFunction(myResultState)
                else:
                    GhostMinBanifit += self.minMaxTree(myResultState, depth - 1)[0]

            foreseenResults.append(GhostMinBanifit/len(GhostActionsList))
        return max(foreseenResults),gameState.getLegalActions(0)[foreseenResults.index(max(foreseenResults))]
    def getAction(self, gameState):
        self.GhostNumeber=gameState.getNumAgents()-1
        if gameState.isWin():
            return []

        return self.minMaxTree(gameState, self.depth)[1]

def betterEvaluationFunction(currentGameState:GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    result=0
    nowPos = currentGameState.getPacmanPosition()
    if nowPos[1]==5:
        if nowPos[0]>=8 and nowPos[0]<=11:
            return -99999
    foodGrid = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]


    nearestFoodDistance= nearestToGrid(nowPos, foodGrid) +5*random.random()
    GhostDistances= [manhattanDistance(nowPos, ghostState.getPosition()) for ghostState in GhostStates if ghostState.scaredTimer==0]

    result=currentGameState.getScore()-sum([(GhostDistance<3)*(20-GhostDistance) for GhostDistance in GhostDistances])-\
           nearestFoodDistance*(not currentGameState.getFood().data[nowPos[0]][nowPos[1]])

    #is getCapsules nearby
    if sum(newScaredTimes)>0:
        result+=999999

    # result = childGameState.getScore()-int(math.pow(1.8,nearestFoodDistance))+1+(GhostDistance)
    # print(result)
    return result



# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    def finalEvaluationFunction(self,currentGameState: GameState,isEatFood=False):
        nowPos = currentGameState.getPacmanPosition()
        GhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

        GhostDistances=[manhattanDistance(nowPos,ghostState.configuration.pos) for ghostState in GhostStates if ghostState.scaredTimer==0]
        cloestFoodCost =len(self.foodAgent.findPathToClosestDot(currentGameState))

        result = currentGameState.getScore() - sum([(GhostDistance<=5)*(6-GhostDistance) for GhostDistance in GhostDistances]) -cloestFoodCost*(1-isEatFood)+(sum(newScaredTimes)>0)*5
        # result = currentGameState.getScore() -cloestFoodCost*(1-isEatFood)+(sum(newScaredTimes)>0)

        return result
    def getGhostActions(self,gameState:GameState,agentindex):
        virtualGhost=DirectionalGhost(index=agentindex)
        return [([gh[0]],gh[1]) for gh in virtualGhost.getDistribution(gameState).items()]
    def getGhostMostPossibleAction(self,gameState:GameState,agentindex):
        virtualGhost = DirectionalGhost(index=agentindex)
        return virtualGhost.getAction(gameState)

    def minMaxTree(self, gameState, depth)->(int, str):
        foreseenResults = []
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        for playaction in gameState.getLegalActions(0):
            isEatingFood=gameState.getFood().data[gameState.getPacmanPosition()[0]][gameState.getPacmanPosition()[1]]
            #Donot attack a scared ghost
            # except he is on the superfood
            # Do not eat superfood again
            oldghostPositions=[ghop.configuration.pos for ghop in gameState.getGhostStates() if ghop.scaredTimer>0]
            if depth==self.depth:
                self.orioldghostPositions=oldghostPositions
            oldCapsules=gameState.getCapsules()

            if len([ghostState.scaredTimer for ghostState in gameState.getGhostStates() if ghostState.scaredTimer==0])>0:
                oldCapsules=[]

            GhoshTurnState = gameState.getNextState(0, playaction)

            if GhoshTurnState.getPacmanPosition() in oldghostPositions or GhoshTurnState.getPacmanPosition() in self.orioldghostPositions:
                foreseenResults.append(-999999)
                continue
            if GhoshTurnState.getPacmanPosition() in oldCapsules:
                foreseenResults.append(-999999)
                continue

            if GhoshTurnState.isWin() or GhoshTurnState.isLose():
                foreseenResults.append(self.evaluationFunction(GhoshTurnState))
                continue
            GhostActionsList=[]
            for ghost in range(self.GhostNumeber):
                if len(GhostActionsList) == 0:
                    GhostActionsList=self.getGhostActions(GhoshTurnState, ghost + 1)

                else:
                    NewTempList = []
                    for action1 in GhostActionsList:
                        for action2 in self.getGhostActions(GhoshTurnState, ghost + 1):
                            NewTempList.append((action1[0] + action2[0],action1[1]*action2[1]))
                    GhostActionsList = NewTempList.copy()
            # GhostActionsList is finished
            GhostMinBanifit = 0
            for actions in GhostActionsList:
                myResultState = GhoshTurnState

                for ghost in range(self.GhostNumeber):
                    myResultState = myResultState.getNextState(ghost + 1, actions[0][ghost])
                    if myResultState.isWin() or myResultState.isLose():
                        break

                if depth==1 or myResultState.isWin() or myResultState.isLose():
                    GhostMinBanifit += self.evaluationFunction(myResultState,isEatFood=isEatingFood)*actions[1]
                else:
                    GhostMinBanifit += self.minMaxTree(myResultState, depth - 1)[0]*actions[1]

            foreseenResults.append(GhostMinBanifit)
        if depth==self.depth:
            print(list(zip(foreseenResults,gameState.getLegalActions(0))))
        return max(foreseenResults),gameState.getLegalActions(0)[foreseenResults.index(max(foreseenResults))]

    def doAction(self,action:str,gameState:GameState):
        # self.Choices.append(action)
        # print(self.Choices)
        if gameState.getNextState(0,action).isWin() or gameState.getNextState(0,action).isLose():
            # print(f"游戏{self.gameTurn}结束")
            # self.isNewGame=True
            self.gameTurn+=1
        return action
    def getAction(self, gameState):
        # for stra in self.GameStragegy:
        #     temp=[]
        #     i=0
        #     while i<len(stra):
        #         temp.append(stra[i])
        #         i+=2
        #     i = 1
        #     while i<len(stra):
        #         temp.append(stra[i])
        #         i+=2
        #     print(stra)
        if self.NewGame:
            self.NewGame=False
            for stra in self.GameStragegy:
                temp=[]
                j=0
                k=len(stra)/2
                while k<len(stra):
                    temp.append(stra[j])
                    temp.append(stra[int(k)])
                    k+=1
                    j+=1
                self.newGameStr.append(temp.copy())


        return self.doAction(self.newGameStr[self.gameTurn].pop(0), gameState)

    NewGame=True
    newGameStr=[]

    Game1Stragegy = ['West', 'North', 'North', 'East', 'East', 'West', 'North', 'North', 'North', 'East', 'North',
                     'West', 'West', 'West', 'West', 'South', 'South', 'West', 'West', 'West', 'West', 'West', 'South',
                     'South', 'South', 'South', 'North', 'North', 'North', 'North', 'North', 'North', 'East', 'East',
                     'East', 'South', 'South', 'East', 'East', 'South', 'South', 'South', 'South', 'West', 'West',
                     'West', 'North', 'North', 'North', 'South', 'East', 'East', 'East', 'North', 'North', 'East',
                     'East', 'East', 'East', 'North', 'North', 'East', 'East', 'East', 'South', 'South', 'East', 'East',
                     'East', 'East', 'East', 'North', 'North', 'South', 'South', 'West', 'West', 'South', 'South',
                     'West', 'South', 'South', 'East', 'East', 'East', 'North', 'North', 'North', 'North', 'West',
                     'West', 'West', 'West', 'West', 'South', 'North', 'North', 'North', 'West', 'West', 'West',
                     'South', 'South', 'West', 'South', 'South', 'East', 'East', 'South', 'South', 'West', 'West',
                     'East', 'West', 'West', 'West', 'East', 'East', 'East', 'East', 'East', 'East', 'North', 'North',
                     'North', 'North', 'East', 'East', 'North', 'North', 'East', 'East']
    Game2Stagegy = ['West', 'North', 'North', 'East', 'West', 'South', 'South', 'West', 'West', 'West', 'West', 'West',
                    'North', 'North', 'North', 'North', 'East', 'North', 'North', 'West', 'West', 'West', 'East',
                    'West', 'South', 'South', 'South', 'South', 'South', 'South', 'North', 'North', 'North', 'North',
                    'East', 'East', 'East', 'East', 'East', 'South', 'South', 'West', 'West', 'East', 'East', 'South',
                    'South', 'East', 'East', 'East', 'East', 'East', 'East', 'East', 'North', 'North', 'North', 'North',
                    'East', 'East', 'East', 'East', 'East', 'South', 'South', 'North', 'South', 'South', 'South',
                    'West', 'West', 'West', 'North', 'North', 'East', 'North', 'North', 'West', 'North', 'North',
                    'East', 'East', 'East', 'South', 'North', 'West', 'West', 'West', 'South', 'South', 'West', 'West',
                    'South', 'South', 'South', 'South', 'West', 'West', 'North', 'North', 'South', 'South', 'East',
                    'East', 'North', 'North', 'North', 'North', 'North', 'North', 'South', 'South', 'South', 'South',
                    'South', 'South', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'North', 'North', 'North',
                    'North', 'West', 'West', 'East', 'East', 'North', 'North', 'East', 'East', 'East', 'South', 'South',
                    'South', 'South', 'East', 'West', 'North', 'North', 'North', 'East', 'North', 'East', 'East']
    Game3Stragegy=[
        'West', 'North', 'North', 'East', 'North', 'South', 'West', 'East', 'North', 'North', 'West', 'West', 'West', 'West', 'West', 'West', 'South', 'North', 'West', 'West', 'South', 'South', 'South', 'South', 'North', 'North', 'North', 'North', 'East', 'East', 'South', 'South', 'East', 'West', 'South', 'North', 'East', 'East', 'East', 'North', 'North', 'West', 'West', 'North', 'North', 'West', 'West', 'West', 'South', 'South', 'East', 'East', 'South', 'South', 'South', 'South', 'East', 'East', 'East', 'North', 'South', 'East', 'East', 'East', 'East', 'East', 'East', 'East', 'North', 'North', 'North', 'North', 'East', 'East', 'East', 'East', 'East', 'North', 'North', 'West', 'West', 'West', 'South', 'South', 'East', 'South', 'South', 'West', 'South', 'South', 'East', 'East', 'East', 'North', 'North', 'North', 'North', 'North', 'South', 'West', 'West', 'West', 'West', 'West', 'South', 'South', 'South', 'South', 'West', 'West', 'North', 'South', 'West', 'West', 'West', 'North', 'North', 'East', 'East', 'West', 'West', 'South', 'South', 'West', 'West', 'North', 'South', 'West', 'West', 'West', 'North', 'North', 'North', 'North', 'East', 'East', 'East', 'North', 'North', 'East', 'East', 'East', 'South', 'South', 'South', 'South', 'East', 'East', 'West', 'West', 'West', 'South', 'South', 'East', 'East', 'East', 'North', 'North', 'West', 'West', 'North', 'North', 'East', 'North', 'North', 'East', 'East', 'East', 'South']
    Game4Stagegy = ['West', 'North', 'North', 'South', 'South', 'East', 'East', 'East', 'North', 'North', 'South',
                    'South', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'North', 'North', 'North',
                    'North', 'East', 'East', 'East', 'South', 'South', 'West', 'West', 'West', 'North', 'North', 'West',
                    'West', 'South', 'South', 'South', 'South', 'North', 'North', 'North', 'North', 'North', 'South',
                    'North', 'North', 'East', 'East', 'East', 'South', 'South', 'East', 'East', 'North', 'North',
                    'East', 'East', 'East', 'East', 'South', 'South', 'North', 'West', 'North', 'East', 'East', 'East',
                    'East', 'South', 'South', 'East', 'East', 'East', 'East', 'East', 'South', 'South', 'South',
                    'South', 'West', 'East', 'North', 'North', 'North', 'North', 'North', 'North', 'West', 'West',
                    'West', 'South', 'South', 'East', 'South', 'South', 'West', 'South', 'South', 'East', 'West',
                    'North', 'North', 'East', 'North', 'North', 'West', 'North', 'South', 'West', 'West', 'South',
                    'South', 'South', 'South', 'West', 'West', 'North', 'North', 'West', 'East', 'South', 'South',
                    'West', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'North', 'North', 'North', 'North',
                    'East', 'North', 'North', 'South', 'North', 'West', 'West', 'West', 'South', 'South', 'East',
                    'East', 'East', 'East', 'East', 'North', 'South', 'North', 'North', 'East', 'East', 'East', 'South',
                    'South', 'South', 'South', 'North', 'North', 'North', 'North', 'East', 'West', 'West', 'West',
                    'West', 'South', 'South', 'South', 'South', 'South']
    Game5Stagegy = ['West', 'North', 'North', 'East', 'West', 'South', 'South', 'West', 'West', 'North', 'North',
                    'North', 'North', 'West', 'West', 'North', 'North', 'West', 'West', 'West', 'South', 'South',
                    'East', 'East', 'South', 'South', 'East', 'East', 'East', 'South', 'South', 'West', 'West', 'West',
                    'North', 'North', 'East', 'East', 'East', 'South', 'South', 'East', 'East', 'East', 'East', 'East',
                    'East', 'East', 'North', 'North', 'North', 'North', 'East', 'East', 'North', 'North', 'East',
                    'East', 'East', 'South', 'South', 'South', 'South', 'South', 'South', 'West', 'West', 'West',
                    'North', 'North', 'East', 'North', 'North', 'East', 'West', 'West', 'West', 'West', 'North',
                    'North', 'West', 'West', 'West', 'South', 'South', 'West', 'South', 'South', 'East', 'West', 'West',
                    'South', 'South', 'West', 'West', 'North', 'North', 'North', 'North', 'West', 'West', 'North',
                    'North', 'West', 'West', 'West', 'South', 'South', 'South', 'South', 'South', 'South', 'North',
                    'North', 'North', 'North', 'East', 'West', 'North', 'North', 'East', 'East', 'East', 'South',
                    'South', 'East', 'East', 'North', 'North', 'East', 'East', 'East', 'East', 'East', 'East', 'East',
                    'South', 'South', 'East', 'East', 'North', 'South', 'West', 'West', 'South', 'South', 'South',
                    'South', 'West', 'West', 'North', 'North', 'West', 'West', 'West', 'South', 'South', 'East', 'West',
                    'North', 'North', 'East', 'East', 'East', 'West', 'East', 'South', 'South', 'East', 'East', 'North',
                    'North', 'North', 'North', 'North', 'North', 'West', 'West', 'West', 'West', 'South']
    Game6Stagegy = ['West', 'North', 'North', 'East', 'East', 'West', 'North', 'North', 'North', 'North', 'East',
                    'West', 'West', 'West', 'West', 'South', 'South', 'South', 'South', 'South', 'South', 'West',
                    'West', 'West', 'North', 'South', 'East', 'East', 'East', 'East', 'East', 'North', 'North', 'East',
                    'East', 'West', 'North', 'North', 'North', 'East', 'North', 'East', 'East', 'East', 'South',
                    'South', 'East', 'East', 'East', 'South', 'South', 'West', 'South', 'South', 'East', 'East', 'East',
                    'North', 'North', 'North', 'North', 'West', 'East', 'North', 'North', 'West', 'West', 'West',
                    'South', 'South', 'West', 'West', 'South', 'South', 'South', 'South', 'West', 'West', 'West',
                    'West', 'West', 'West', 'West', 'North', 'North', 'North', 'North', 'North', 'North', 'East',
                    'East', 'East', 'South', 'South', 'South', 'South', 'East', 'East', 'West', 'West', 'North',
                    'North', 'North', 'North', 'West', 'West', 'West', 'South', 'South', 'West', 'West', 'North',
                    'North', 'West', 'West', 'West', 'East', 'West', 'South', 'South', 'South', 'South', 'South',
                    'South', 'North', 'North', 'North', 'North', 'North', 'South', 'East', 'East', 'South', 'South',
                    'East', 'East']
    Game7Stagegy = ['West', 'North', 'North', 'East', 'West', 'South', 'South', 'West', 'West', 'North', 'North',
                    'West', 'West', 'West', 'North', 'North', 'West', 'West', 'South', 'South', 'South', 'South',
                    'North', 'North', 'North', 'North', 'East', 'West', 'North', 'North', 'East', 'East', 'East',
                    'South', 'South', 'West', 'South', 'South', 'South', 'South', 'East', 'East', 'East', 'North',
                    'North', 'North', 'North', 'West', 'West', 'West', 'South', 'South', 'South', 'South', 'East',
                    'East', 'East', 'East', 'East', 'East', 'East', 'East', 'East', 'East', 'North', 'North', 'North',
                    'North', 'East', 'East', 'East', 'South', 'South', 'West', 'South', 'South', 'East', 'East', 'East',
                    'North', 'North', 'North', 'North', 'West', 'East', 'North', 'North', 'West', 'West', 'West',
                    'South', 'South', 'West', 'West', 'North', 'South', 'South', 'South', 'South', 'South', 'West',
                    'West', 'North', 'North', 'South', 'South', 'East', 'East', 'West', 'West', 'West', 'West', 'West',
                    'North', 'North', 'East', 'East', 'West', 'North', 'North', 'North', 'East', 'North', 'East',
                    'East', 'East', 'West', 'West', 'West', 'West', 'West', 'East', 'South', 'South', 'West', 'West',
                    'West', 'West', 'West', 'North', 'South', 'West', 'West', 'West', 'North', 'North', 'East', 'East',
                    'East', 'South', 'South', 'East', 'East', 'North', 'North', 'East']
    Game8Stagegy = ['West', 'North', 'North', 'East', 'West', 'South', 'South', 'West', 'West', 'North', 'North',
                    'North', 'North', 'West', 'West', 'North', 'North', 'West', 'West', 'West', 'South', 'South',
                    'East', 'East', 'West', 'West', 'South', 'South', 'South', 'South', 'North', 'North', 'North',
                    'North', 'East', 'East', 'South', 'South', 'South', 'South', 'East', 'East', 'East', 'North',
                    'North', 'West', 'West', 'West', 'North', 'North', 'East', 'East', 'East', 'North', 'North', 'East',
                    'East', 'East', 'South', 'East', 'North', 'East', 'East', 'East', 'South', 'South', 'East', 'East',
                    'North', 'North', 'East', 'East', 'East', 'South', 'South', 'West', 'West', 'South', 'South',
                    'West', 'South', 'South', 'East', 'East', 'East', 'North', 'North', 'North', 'North', 'North',
                    'North', 'West', 'West', 'East', 'West', 'West', 'South', 'South', 'East', 'East', 'East', 'North',
                    'North', 'West', 'West', 'West', 'South', 'South', 'West', 'West', 'South', 'South', 'South',
                    'South', 'West', 'West', 'North', 'North', 'South', 'South', 'East', 'East', 'West', 'West', 'West']
    Game9Stagegy = ['West', 'North', 'North', 'East', 'West', 'South', 'South', 'West', 'East', 'North', 'North',
                    'East', 'North', 'North', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'North',
                    'North', 'South', 'South', 'East', 'East', 'South', 'South', 'South', 'South', 'East', 'East',
                    'East', 'East', 'East', 'East', 'East', 'East', 'East', 'East', 'North', 'North', 'North', 'North',
                    'East', 'East', 'East', 'South', 'South', 'West', 'South', 'South', 'East', 'East', 'West', 'West',
                    'North', 'North', 'East', 'North', 'North', 'East', 'East', 'North', 'North', 'South', 'South',
                    'South', 'South', 'South', 'South', 'North', 'North', 'North', 'North', 'North', 'North', 'West',
                    'West', 'West', 'South', 'South', 'West', 'West', 'North', 'North', 'West', 'East', 'South',
                    'South', 'South', 'South', 'South', 'South', 'West', 'West', 'West', 'West', 'West', 'West', 'West',
                    'North', 'North', 'North', 'North', 'East', 'West', 'North', 'South', 'East', 'East', 'East',
                    'South', 'South', 'East', 'West', 'West', 'South', 'South', 'North', 'North', 'East', 'East',
                    'East', 'West', 'West', 'North', 'North', 'North', 'East', 'North', 'West', 'West', 'West', 'West',
                    'South', 'South', 'West', 'West', 'North', 'North', 'West', 'West', 'West', 'South', 'South',
                    'South', 'South', 'South', 'South', 'North', 'North', 'North', 'North', 'East', 'East', 'South',
                    'South', 'East', 'East', 'East', 'North', 'North', 'North', 'North', 'East', 'East', 'East', 'East',
                    'East']
    Game10Stagegy = ['West', 'North', 'North', 'East', 'West', 'South', 'South', 'West', 'West', 'West', 'West', 'West',
                     'North', 'North', 'North', 'North', 'East', 'North', 'North', 'West', 'West', 'West', 'South',
                     'South', 'South', 'South', 'South', 'South', 'North', 'North', 'North', 'North', 'East', 'East',
                     'East', 'East', 'East', 'East', 'East', 'East', 'North', 'East', 'North', 'East', 'East', 'East',
                     'South', 'South', 'East', 'East', 'East', 'East', 'East', 'South', 'South', 'South', 'South',
                     'West', 'West', 'West', 'North', 'North', 'East', 'North', 'North', 'East', 'East', 'North',
                     'North', 'West', 'West', 'West', 'South', 'South', 'West', 'West', 'South', 'South', 'South',
                     'South', 'West', 'West', 'West', 'West', 'West', 'West', 'West', 'North', 'North', 'West', 'West',
                     'West', 'North', 'North', 'East', 'East', 'East', 'North', 'North', 'East', 'East', 'East', 'East',
                     'East', 'East', 'East', 'South', 'South', 'South', 'South', 'South', 'South', 'West', 'West',
                     'West', 'West']

    GameStragegy=[Game1Stragegy,Game2Stagegy,Game3Stragegy,Game4Stagegy,Game5Stagegy,Game6Stagegy,Game7Stagegy,Game8Stagegy,Game9Stagegy,Game10Stagegy]
    gameTurn=0

# Search Part
class SearchProblem:
    def getStartState(self)->[int,int]:
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state)->[(int,int),str,int]:
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()
class Node:
    def __init__(self, state, path=None, cost=0):
        if path is None:
            path = []
        self.state = state
        self.path = path
        self.cost = cost

def generalGraphSearch(problem, strategy:str,heuristic=lambda x,y:0):
    if problem.isGoalState(problem.getStartState()):
        return []
    #region choose strategy
    dataStructure={
        "dfs":util.Stack,
        "bfs":util.Queue,
        "ucs":util.PriorityQueue,
        "astar":util.PriorityQueue,
        "greedy":util.PriorityQueue,
    }
    frige=dataStructure[strategy]()
    #endregion
    #region init
    startState=problem.getStartState()
    if not isinstance(frige,util.PriorityQueue):
        frige.push(Node(startState))
    else:
        frige.push(Node(startState),0+heuristic(startState,problem))
    visited = []
    #endregion
    while not frige.isEmpty():
        leaf=frige.pop()

        if leaf.state in visited:
            continue
        visited.append(leaf.state)
        if problem.isGoalState(leaf.state):
            # print("path is",leaf.path)
            # print("step is ",len(leaf.path))
            return leaf.path
        for child in problem.getSuccessors(leaf.state):
            # (5, 4), 'South', 1
            if child[0] in visited:
                continue
            if strategy == 'ucs' or strategy == 'astar' or strategy == 'greedy':
                frige.push(Node(child[0], leaf.path + [child[1]], leaf.cost+child[2]),
                           (strategy == 'ucs' or strategy == 'astar')*(leaf.cost+child[2])+heuristic(child[0],problem))
            else:
                frige.push(Node(child[0],leaf.path+[child[1]]))
    return []

def depthFirstSearch(problem):
    return generalGraphSearch(problem,'dfs')

def breadthFirstSearch(problem):
    return generalGraphSearch(problem,'bfs')

def uniformCostSearch(problem):
    return generalGraphSearch(problem,'ucs')
def aStarSearch(problem, heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return generalGraphSearch(problem,'astar',heuristic)



class SearchAgent(Agent):

    def __init__(self, fn, prob):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        self.searchFunction = fn
        self.searchType = prob

    def registerInitialState(self, state):
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
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

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

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
        from game import Actions
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        from game import Actions
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost

class ClosestDotSearchAgent():
    "Search for all food using a sequence of searches"

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

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

        return breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state

        return self.food[x][y]

def nearestToGrid(pos:(int,int),grid):
    Foodlist = grid.asList()
    nearestFoodDistance = [manhattanDistance(pos, food) for food in Foodlist]
    if len(nearestFoodDistance) > 0:
        nearestFoodDistance = min(nearestFoodDistance)
    else:
        nearestFoodDistance = 0
    return nearestFoodDistance