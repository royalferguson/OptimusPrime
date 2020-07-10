from OptimusPrime.solvers import BaseSolver
from scipy.optimize import basinhopping
from OptimusPrime.utils.functions.fileio import loggedToCsv
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 
import pandas as pd


def _objective_function(func, log_cb=None):
	def func_wrapper(x, *args):
		score = func(x, *args)
		if log_cb:
			log_cb(x, score)
			pass
		return score
	return func_wrapper

class BasinhoppingSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.tol = 0
		self.lowest_so_far = [np.inf,np.inf]
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, niter=1000, **kwargs):
		if 'tol' in kwargs:
			self.tol = kwargs.pop('tol')
		kwargs.update({'niter' : niter})
		kwargs.update({'callback' : self.callback})
		objective_func = _objective_function(fun, log_cb=self.pickle_data)
		a = basinhopping(objective_func, **kwargs)
		loggedToCsv('basinhopping', self.intermitentData)
		return a

	def callback(self, xk, f, accept):
		self.log_data(xk, f, accept)
		if self.check_tolerance():
			return True
		if f < self.lowest_so_far[1]:
			self.lowest_so_far = [xk,f]
		return False

	def check_tolerance(self):
		if self.tol is not None:
			if len(self.intermitentData) >= 2 and self.intermitentData.iloc[len(self.intermitentData)-1,1] != self.lowest_so_far[1] and abs(self.intermitentData.iloc[len(self.intermitentData)-1,1] - self.lowest_so_far[1]) < self.tol:
				print("The last two entries are: ====================")
				print(self.lowest_so_far,self.intermitentData.tail(1))
				print(self.intermitentData.tail(2))
				return True
		return False

	def log_data(self, x, f, accept):
		# log data is used by check_tolerance
		s = pd.Series([x,f], index=['dv','score'])
		
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)
		
	def pickle_data(self, x, f):
		#  Added so that display data is driven from the obj function wrapper instead of the callback
		s = pd.Series([x,f], index=['dv','score'])
		s.add_to_pickle('optimization_data.pkl')
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)