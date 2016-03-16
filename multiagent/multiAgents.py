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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
				"""
						A reflex agent chooses an action at each choice point by examining
						its alternatives via a state evaluation function.

						The code below is provided as a guide.  You are welcome to change
						it in any way you see fit, so long as you don't touch our method
						headers.
				"""


				def getAction(self, gameState):
								"""
								You do not need to change this method, but you're welcome to.

								getAction chooses among the best options according to the evaluation function.

								Just like in the previous project, getAction takes a GameState and returns
								some Directions.X for some X in the set {North, South, West, East, Stop}
								"""
								# Collect legal moves and successor states
								legalMoves = gameState.getLegalActions()

								# Choose one of the best actions
								scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
								bestScore = max(scores)
								bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
								chosenIndex = random.choice(bestIndices) # Pick randomly among the best

								"Add more of your code here if you want to"

								return legalMoves[chosenIndex]

				def evaluationFunction(self, currentGameState, action):
								"""
								Design a better evaluation function here.

								The evaluation function takes in the current and proposed successor
								GameStates (pacman.py) and returns a number, where higher numbers are better.

								The code below extracts some useful information from the state, like the
								remaining food (newFood) and Pacman position after moving (newPos).
								newScaredTimes holds the number of moves that each ghost will remain
								scared because of Pacman having eaten a power pellet.

								Print out these variables to see what you're getting, then combine them
								to create a masterful evaluation function.
								"""
								# Useful information you can extract from a GameState (pacman.py)
								successorGameState = currentGameState.generatePacmanSuccessor(action)
								newPos = successorGameState.getPacmanPosition()
								newFood = successorGameState.getFood()
								newGhostStates = successorGameState.getGhostStates()
								newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

								#print currentGameState
								#print successorGameState.getScore() 
								#print newPos
								#print newFood.asList()
								#print newScaredTimes

								closestFoodDistance = 1000
								for (x,y) in newFood.asList():
										foodmanhattan = util.manhattanDistance(newPos, (x,y))
										if foodmanhattan < closestFoodDistance:
												closestFoodDistance = foodmanhattan

								ghostPosition = successorGameState.getGhostPositions()[0]
								ghostDistance = util.manhattanDistance(newPos, ghostPosition)

								score = 0
								if successorGameState.isWin():
										return float("inf")
								if ghostDistance < 5:
										if ghostDistance < 1:
												score-= 5000
										else:
												score -= 5000/ghostDistance
								if successorGameState.getNumFood() < currentGameState.getNumFood():
										score += 500
								if newPos in successorGameState.getCapsules():
										score += 500
								score -= 10*closestFoodDistance
								return score

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

				def getAction(self, gameState):
								"""
										Returns the minimax action from the current gameState using self.depth
										and self.evaluationFunction.

										Here are some method calls that might be useful when implementing minimax.

										gameState.getLegalActions(agentIndex):
												Returns a list of legal actions for an agent
												agentIndex=0 means Pacman, ghosts are >= 1

										gameState.generateSuccessor(agentIndex, action):
												Returns the successor game state after an agent takes an action

										gameState.getNumAgents():
												Returns the total number of agents in the game

										gameState.isWin():
												Returns whether or not the game state is a winning state

										gameState.isLose():
												Returns whether or not the game state is a losing state
								"""
								def minimax(gameState, depth, agent):
										if gameState.isWin() or gameState.isLose() or depth == 0:
												return self.evaluationFunction(gameState)
										if agent == 0:  #pacmans turn
												PacBestVal = -float('inf')
												PacActions = gameState.getLegalActions(0)
												for action in PacActions:
														nextState = gameState.generateSuccessor(0,action)
														actionVal = minimax(nextState, depth, 1)
														PacBestVal = max(actionVal, PacBestVal)
												return PacBestVal
										else:
												GhostBestVal = float('inf')
												GhostActions = gameState.getLegalActions(agent)
												for action in GhostActions:
														nextState = gameState.generateSuccessor(agent, action)
														if agent == (gameState.getNumAgents()-1):           #last agent
																actionVal = minimax(nextState, depth-1, 0)
														else:
																actionVal = minimax(nextState, depth, agent+1)
														GhostBestVal = min(actionVal, GhostBestVal)
												return GhostBestVal

								PacActions = gameState.getLegalActions(0)
								bestAction = None
								bestActionValue = None
								for action in PacActions:
										nextState = gameState.generateSuccessor(0,action)
										actionValue = minimax(nextState, self.depth, 1)
										if (bestAction == None) or (actionValue > bestActionValue):
												bestAction = action
												bestActionValue = actionValue
								return bestAction

								util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
				"""
						Your minimax agent with alpha-beta pruning (question 3)
				"""

				def getAction(self, gameState):
								"""
										Returns the minimax action using self.depth and self.evaluationFunction
								"""
								"*** YOUR CODE HERE ***"
								def alphabeta(gameState, depth, agent, A, B):
										if gameState.isWin() or gameState.isLose() or depth == 0:
												return self.evaluationFunction(gameState)
										if agent == 0:  #pacmans turn
												PacBestVal = -float('inf')
												PacActions = gameState.getLegalActions(0)
												for action in PacActions:
														nextState = gameState.generateSuccessor(0,action)
														actionVal = alphabeta(nextState, depth, 1, A, B)
														PacBestVal = max(actionVal, PacBestVal)
														A = max(A, PacBestVal)
														if PacBestVal > B:
																break
												return PacBestVal
										else:
												GhostBestVal = float('inf')
												GhostActions = gameState.getLegalActions(agent)
												for action in GhostActions:
														nextState = gameState.generateSuccessor(agent, action)
														if agent == (gameState.getNumAgents()-1):           #last agent
																actionVal = alphabeta(nextState, depth-1, 0, A, B)
														else:
																actionVal = alphabeta(nextState, depth, agent+1, A, B)
														GhostBestVal = min(actionVal, GhostBestVal)
														B = min (B, GhostBestVal)
														if GhostBestVal < A:
																break
												return GhostBestVal


								PacActions = gameState.getLegalActions(0)
								bestAction = None
								bestActionValue = -float('inf')
								alpha = -float('inf')
								beta = float('inf')
								for action in PacActions:
										nextState = gameState.generateSuccessor(0,action)
										actionValue = alphabeta(nextState, self.depth, 1, alpha, beta)
										if (actionValue > bestActionValue):
												bestAction = action
												bestActionValue = actionValue
										alpha = max(alpha, bestActionValue)
								return bestAction
								util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
				"""
						Your expectimax agent (question 4)
				"""

				def getAction(self, gameState):
								"""
										Returns the expectimax action using self.depth and self.evaluationFunction

										All ghosts should be modeled as choosing uniformly at random from their
										legal moves.
								"""
								def minimax(gameState, depth, agent):
										if gameState.isWin() or gameState.isLose() or depth == 0:
												return self.evaluationFunction(gameState)
										if agent == 0:  #pacmans turn
												PacBestVal = -float('inf')
												PacActions = gameState.getLegalActions(0)
												for action in PacActions:
														nextState = gameState.generateSuccessor(0,action)
														actionVal = minimax(nextState, depth, 1)
														PacBestVal = max(actionVal, PacBestVal)
												return PacBestVal
										else:
												GhostBestVal = float('inf')
												GhostActions = gameState.getLegalActions(agent)
												numActions = len(GhostActions)
												sumActions = 0
												for action in GhostActions:
														nextState = gameState.generateSuccessor(agent, action)
														if agent == (gameState.getNumAgents()-1):           #last agent
																actionVal = minimax(nextState, depth-1, 0)
														else:
																actionVal = minimax(nextState, depth, agent+1)
														sumActions += actionVal
														#GhostBestVal = min(actionVal, GhostBestVal)
												return float(sumActions)/float(numActions)

								PacActions = gameState.getLegalActions(0)
								bestAction = None
								bestActionValue = None
								for action in PacActions:
										nextState = gameState.generateSuccessor(0,action)
										actionValue = minimax(nextState, self.depth, 1)
										if (bestAction == None) or (actionValue > bestActionValue):
												bestAction = action
												bestActionValue = actionValue
								return bestAction
								util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
				"""
						Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
						evaluation function (question 5).

						# # DESCRIPTION: I decided to go with the method of creating a weighted linear combination of
						#  the current game state properties. To incentivize pacman to continually 
						# # eat food, the weighted sum includes the reciprocal of the number of food pellets left
						#  times a constant factor. I also encouraged pacman to stay away from ghosts by 
						# # subtracting the reciprocal of the ghost's distance. When the ghost got too close to 
						# pacman to within a threshold, the penalty for the state is even higher. I also 
						# # created incentives for pacman to clear out the power pellets by subtracting a constant
						#  factor times the number of power pellets left. I also used the reciprocal of
						# #  the power pellet distance to encourage pacman to move towards power pellets, much like
						#  I incentivized him to eat food. Of course, I had to adjust and test all 
						# #  these weights until the met the auto grader requirements.
				"""
				"*** YOUR CODE HERE ***"
				closestFoodDistance = 1000
				pacmanPostion = currentGameState.getPacmanPosition()
				foodList = currentGameState.getFood().asList()
				capsulePositions = currentGameState.getCapsules()

				for (x,y) in foodList:
						foodmanhattan = util.manhattanDistance(pacmanPostion, (x,y))
						if foodmanhattan < closestFoodDistance:
								closestFoodDistance = foodmanhattan

				ghostPositions = currentGameState.getGhostPositions()
				ghostDistance = util.manhattanDistance(pacmanPostion, ghostPositions[0])
				
				#print ghostPositions
				closestCapsuleDistance = 1000
				capsulecount = 0
				for location in capsulePositions:
						capsulecount+=1
						capsulemanhattan = util.manhattanDistance(pacmanPostion, location)
						if capsulemanhattan < closestCapsuleDistance:
								closestCapsuleDistance = capsulemanhattan

				score = 0
				score =  -10*(closestFoodDistance+1) - 400/(ghostDistance+1) + 300/(1+closestCapsuleDistance) - 1000*(capsulecount) - 300*len(foodList) 


				if ghostDistance < 3:
						score -= ghostDistance*3000
				if currentGameState.isWin():
						score += 10000
				return score

				util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

