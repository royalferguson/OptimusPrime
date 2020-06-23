from OptimusPrime.solvers import BaseSolver
from scipy.optimize import minimize
from functools import partial
import numpy as np 
import pandas as pd
import seaborn as sb 
import matplotlib.pyplot as plt 

class MinimizeSolver(BaseSolver):

	def __init__(self):
		super().__init__()
		self.intermitentData = pd.DataFrame()
	
	def solve(self, fun, maxiter=1000, **kwargs):
		kwargs.update({'options' : {'maxiter': maxiter}})
		kwargs['callback'] = self.callback_
		self.fun = fun
		return minimize(fun, **kwargs)

	def callback_(self, xk):
		f = self.fun(xk)
		self.log_intermediate_data(xk, f)
		s = pd.Series([xk,f], index=['dv','score'])
		s.add_to_pickle('optimization_data.pkl')

	def log_intermediate_data(self, xk, f):
		pass
