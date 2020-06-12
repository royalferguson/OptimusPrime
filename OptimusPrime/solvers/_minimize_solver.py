from OptimusPrime.solvers import BaseSolver
from scipy.optimize import minimize
from functools import partial
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 

def minimize_objective_function(func, callback=None):
	def func_wrapper(x, *args):
		score = func(x, *args):
		if callback:
			callback(x, score)
		return score
	return func_wrapper


class MinimizeSolver(BaseSolver):
	def __init__(self,method):
		self.minimize = partial(minmize, method=method, callback=None)

	def solve(self, fun, x0, bounds = None, maxiter=1000, **kwargs):
		if 'options' in kwargs:
			kwargs['options'].update({'maxiter' : maxiter})
		else:
			kwargs['minimizer_kwargs'] = {'maxiter' : maxiter}

	objective_func = minimize_objective_function(fun,self.callback)
	return self.minimize(objective_func, x0, bounds = bounds, **kwargs)

	def callback_(self, xk, f):
		self.log_intermediate_data(xk, f)

	def log_intermediate_data(self, xk, f):
		pass
