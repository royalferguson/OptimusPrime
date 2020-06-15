from OptimusPrime.solvers import BaseSolver
from scipy.optimize import minimize
from functools import partial
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 

class MinimizeSolver(BaseSolver):
	
	def solve(self, fun, maxiter=1000, **kwargs):
		kwargs.update({'maxiter' : maxiter})
		if 'callback' not in kwargs:
			kwargs['callback'] = self.callback_
		self.fun = fun
		return minimize(fun, **kwargs)

	def callback_(self, xk):
		f = self.fun(xk)
		self.log_intermediate_data(xk, f)

	def log_intermediate_data(self, xk, f):
		pass
