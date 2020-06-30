from OptimusPrime.solvers import BaseSolver
from scipy.optimize import differential_evolution
import numpy as np 
import pandas as pd
import seaborn as sb 
import matplotlib.pyplot as plt
from OptimusPrime.logger import *

def _objective_function(func, log_cb=None):
	def func_wrapper(x, *args):
		score = func(x, *args)
		if log_cb:
			log_cb(x, score)
		return score
	return func_wrapper

class DifferentialEvolutionSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, **kwargs):
		self.fun = fun
		if 'x0' in kwargs:
			x0  =  kwargs.pop('x0')
			m = kwargs.get('popsize', 15)  # get from kwargs or use scipy default
			popsize= kwargs['popsize']
			len_x0 = len(x0)

			print("x0 len:  ", len_x0)
			print("popsize: ", popsize)
			print("m:  ", m)
			print("np.shape: ", np.shape(x0))
			x0=x0.transpose()
			print("transpose np.shape: ", np.shape(x0))

			if np.shape(x0) != (m, len_x0):
				#  If x0 does not have shape of (m, len(x0)) - revert to latinhypercube
				#  Where m is the #population * the number of decision variables
				print('reverting to latinhypercube')
				x0='latinhypercube'
				#logger.warning(fmt('warning', 'initial population array does not have shape (m,len(x0))  defaulting to latinhypercube'))
			kwargs.update({'init' : x0})
		objective_func = _objective_function(fun, log_cb=self.log_data)
		return differential_evolution(objective_func, **kwargs)


	def log_data(self, xk, f):
		s = pd.Series([xk,self.fun(xk)], index=['dv','score'])
		s.add_to_pickle('optimization_data.pkl')
		self.intermitentData = self.intermitentData.append(s, ignore_index=True)
		logger.data(s.to_json()) 

