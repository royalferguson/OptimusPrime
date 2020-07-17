from OptimusPrime.solvers import BaseSolver
from scipy.optimize import dual_annealing
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt
import pandas as pd
from OptimusPrime.utils.functions.fileio import loggedToCsv

def _objective_function(func, log_cb=None):
	def func_wrapper(x, *args):
		score = func(x, *args)
		if log_cb:
			log_cb(x, score)
		return score
	return func_wrapper

class DualAnnealingSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.tol = None
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, maxiter=1000, **kwargs):
		if 'tol' in kwargs:
			self.tol = kwargs.pop('tol')
		kwargs.update({'maxiter' : maxiter})
		kwargs.update({'callback' : self.callback})
		objective_func = _objective_function(fun, log_cb=self.pickle_data)
		a = dual_annealing(objective_func, **kwargs)
		loggedToCsv('dual_annealing', self.intermitentData)
		return a

	def callback(self, xk, f, accept):
		self.log_data(xk, f, accept)
		if self.check_tolerance():
			return True
		return False

	def check_tolerance(self):
		if self.tol is not None:
			if len(self.intermitentData) >= 2 and abs(self.intermitentData.iloc[len(self.intermitentData)-1,1] - self.intermitentData.iloc[len(self.intermitentData)-2,1]) < self.tol and self.intermitentData.iloc[len(self.intermitentData)-1,1] != self.intermitentData.iloc[len(self.intermitentData)-2,1] :
				return True
		return False

	def log_data(self, x, f, accept):
		# log data is used by check_tolerance
		s = pd.Series([x,f], index=['dv','score'])
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)
		
	def pickle_data(self, x, f):
		#  Added so that display data is driven from the obj function wrappr instead of the callback
		s = pd.Series([x,f], index=['dv','score'])
		s.add_to_pickle('optimization_data.pkl')
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)