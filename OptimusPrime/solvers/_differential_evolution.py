from OptimusPrime.solvers import BaseSolver
from scipy.optimize import differential_evolution
import numpy as np 
import pandas as pd
import seaborn as sb 
from OptimusPrime.utils.functions.fileio import loggedToCsv
import matplotlib.pyplot as plt
from OptimusPrime.logger import *
import pickle
from functools import partial

def func_wrapper(fun, x, *args, log_cb = None):
	score = fun(x, *args)
	if log_cb:
		log_cb(x, score)
	return score

class DifferentialEvolutionSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, **kwargs):
		self.fun = fun
		log_cb = None		
		if 'x0' in kwargs:
			x0  =  kwargs.pop('x0')

			x0 = np.asarray(x0)   # ensure it's an array.
			
			if x0.ndim == 2:
				len_x0=x0.shape[1]
			else: 
				len_x0 = len(x0)

			# A multiplier for setting the total population size. The population has popsize * len(x) individuals.
			popsize= kwargs.get('popsize', 15)
			m = kwargs.get('popsize', 15) * len_x0   # get from kwargs or use scipy default
			if np.shape(x0) != (m, len_x0):
				#  If x0 does not have shape of (m, len(x0)) - revert to latinhypercube
				#  Where m is the #population * the number of decision variables
				print('reverting to latinhypercube')
				x0='latinhypercube'
				#logger.warning(fmt('warning', 'initial population array does not have shape (m,len(x0))  defaulting to latinhypercube'))
			kwargs.update({'init' : x0})
		objective_func = partial(func_wrapper,fun, log_cb = self.log_data)
		a = differential_evolution(objective_func, **kwargs)
		loggedToCsv('differential_evolution', self.intermitentData)
		return a

	def log_data(self, xk, f):
		s = pd.Series([xk,self.fun(xk)], index=['dv','score'])
		s.add_to_pickle('optimization_data.pkl')
		self.intermitentData = self.intermitentData.append(s, ignore_index=True)
		logger.data(s.to_json()) 