from OptimusPrime.solvers import BaseSolver
from scipy.optimize import differential_evolution
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 

class DifferentialEvolutionSolver(BaseSolver):
	def __init__(self):
		pass

	def solve(self, fun, kwargs):
		if kwargs['x0']:
			m=len( kwargs['x0']) * kwargs['popsize']
			if np.shape( kwargs['x0']) != (m, len( kwargs['x0'])):
				#  If x0 does not have shape of (m, len(x0)) - revert to latinhypercube
				#  Where m is the #population * the number of decision variables
				 kwargs['x0']='latinhypercube'
		kwargs['init']  =  kwargs.pop('x0')
		return differential_evolution(fun, **kwargs)


	def callback(self, xk, convergence=None):
		self.log_intermediate_data(xk)

	def log_intermediate_data(self, xk):
		pass