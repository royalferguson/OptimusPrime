from OptimusPrime.solvers import BaseSolver
from scipy.optimize import differential_evolution
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 

class DifferentialEvolutionSolver(BaseSolver):
	def __init__(self):
		pass

	def solve(self, fun, x0=None, bounds=None, maxiter=1000, popsize=15, **kwargs):
		if x0:
			m=len(x0) * popsize
			if np.shape(x0) != (m, len(x0)):
				#  If x0 does not have shape of (m, len(x0)) - revert to latinhypercube
				#  Where m is the #population * the number of decision variables
				x0='latinhypercube'

		return differential_evolution(fun,bounds, init=x0, callback=self.callback, maxiter=maxiter, **kwargs)


	def callback(self, xk, convergence=None):
		self.log_intermediate_data(xk)

	def log_intermediate_data(self, xk):
		pass