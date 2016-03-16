# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
	"""
			* Please read learningAgents.py before reading this.*

			A ValueIterationAgent takes a Markov decision process
			(see mdp.py) on initialization and runs value iteration
			for a given number of iterations using the supplied
			discount factor.
	"""
	def __init__(self, mdp, discount = 0.9, iterations = 100):
		"""
			Your value iteration agent should take an mdp on
			construction, run the indicated number of iterations
			and then act according to the resulting policy.

			Some useful mdp methods you will use:
					mdp.getStates()
					mdp.getPossibleActions(state)
					mdp.getTransitionStatesAndProbs(state, action)
					mdp.getReward(state, action, nextState)
					mdp.isTerminal(state)
		"""
		self.mdp = mdp
		self.discount = discount
		self.iterations = iterations
		self.values = util.Counter() # A Counter is a dict with default 0

		# Write value iteration code here
		"*** YOUR CODE HERE ***"
		states = mdp.getStates()
		for i in range(0,iterations):
			preupdatevalues = self.values.copy()
			for state in states:
				actionVals = util.Counter() #make a new counter for possible action
				for action in mdp.getPossibleActions(state):
					for nextState, prob in mdp.getTransitionStatesAndProbs(state,action):
						reward = mdp.getReward(state, action, nextState)
						actionVals[action] += prob*(reward + discount*preupdatevalues[nextState])
				self.values[state] = actionVals[actionVals.argMax()]
		# for i in range(self.iterations):
		# 	newVals=util.Counter()

		# 	for state in self.mdp.getStates():

		# 		bestActionVal=float('-inf')
		# 		possibleActions=self.mdp.getPossibleActions(state)
		# 		if len(possibleActions)>1:
		# 			newVals[state]=0
		# 			for action in possibleActions:
		# 				valSum=0
		# 				tStatesAndProbs=self.mdp.getTransitionStatesAndProbs(state, action)
		# 				for tState, tProb in tStatesAndProbs:
		# 					reward=self.mdp.getReward(state, action, tState)
		# 					valSum[action]+=tProb*(reward+self.discount*self.getValue(tState))


		# 					if bestActionVal<valSum:
		# 						bestActionVal=valSum
		# 						newVals[state]=bestActionVal

		# 	self.values[state] = newVals[newVals.argMax()]
		# for i in range(self.iterations):
	#   			newVals=util.Counter()

	#   			for state in self.mdp.getStates():

	#   				bestActionVal=float('-inf')
	#   				possibleActions=self.mdp.getPossibleActions(state)
	#   				if len(possibleActions)<1:
	#   					newVals[state]=0
	#   				for action in possibleActions:

	#   					valSum=0
	#   					tStatesAndProbs=self.mdp.getTransitionStatesAndProbs(state, action)
	#   					for tState, tProb in tStatesAndProbs:
	#   						reward=self.mdp.getReward(state, action, tState)
	#   						valSum+=tProb*(reward+self.discount*self.getValue(tState))

	#   						if bestActionVal<valSum:
	#   							bestActionVal=valSum
	#   							newVals[state]=bestActionVal

	#   			self.values = newVals

			




	def getValue(self, state):
		"""
			Return the value of the state (computed in __init__).
		"""
		return self.values[state]


	def computeQValueFromValues(self, state, action):
		"""
			Compute the Q-value of action in state from the
			value function stored in self.values.
		"""
		"*** YOUR CODE HERE ***"
		# mdp = self.mdp
		# stateProbList = mdp.getTransitionStatesAndProbs(state, action)
		# Qsum = 0
		# for (nextState, prob) in stateProbList:
		# 	reward = mdp.getReward(state, action, nextState)
		# 	Qsum += prob*(reward+self.discount*self.getValue(nextState))
		# return Qsum
		qVal=0
		tStatesAndProbs=self.mdp.getTransitionStatesAndProbs(state, action)
		for tState, tProb in tStatesAndProbs:
			reward=self.mdp.getReward(state, action, tState)
			qVal+=tProb*(reward+self.discount*self.values[tState])
		return qVal

		util.raiseNotDefined()

	def computeActionFromValues(self, state):
		"""
			The policy is the best action in the given state
			according to the values currently stored in self.values.

			You may break ties any way you see fit.  Note that if
			there are no legal actions, which is the case at the
			terminal state, you should return None.
		"""
		"*** YOUR CODE HERE ***"
		# actions = self.mdp.getPossibleActions(state)
		# maxQ = 0
		# maxAction = None
		# for action in actions:
		# 	Qvalue = self.computeQValueFromValues(state, action)
		# 	if maxQ == 0 or Qvalue > maxQ:
		# 		maxQ = Qvalue
		# 		maxAction = action
		# return maxAction #returns the arg max of q values
		bestAction=None
		bestActionVal=float('-inf')
		possibleActions=self.mdp.getPossibleActions(state)
		if len(possibleActions)<1 or self.mdp.isTerminal(state):
			return None
		for action in possibleActions:
			qVal=self.computeQValueFromValues(state, action)
			if bestActionVal<qVal:
				bestAction=action
				bestActionVal=qVal
		return bestAction

		util.raiseNotDefined()

	def getPolicy(self, state):
		return self.computeActionFromValues(state)

	def getAction(self, state):
		"Returns the policy at the state (no exploration)."
		return self.computeActionFromValues(state)

	def getQValue(self, state, action):
		return self.computeQValueFromValues(state, action)
