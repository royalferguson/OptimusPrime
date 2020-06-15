from OptimusPrime.solvers import BaseSolver
from scipy.optimize import dual_annealing
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt
import pandas as pd

class DualAnnealingSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.tol = 0
		self.intermitentData = pd.DataFrame()
		self.callback_count = 0

	def solve(self, fun, maxiter=1000, **kwargs):
		if 'tol' in kwargs:
			self.tol = kwargs.pop('tol')
		kwargs.update({'maxiter' : maxiter})
		kwargs.update({'callback' : self.log_data})
		return dual_annealing(fun, **kwargs)

	_='''
	def callback(self, xk, f, accept):
		self.log_data(xk, f, accept)
	'''

	def log_data(self, x, f, accept):
		self.callback_count += 1
		s = pd.Series([x,f], index=['dv','score'])
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)
		if len(self.intermitentData) >= 2 and abs(self.intermitentData.iloc[len(self.intermitentData)-1,1] - self.intermitentData.iloc[len(self.intermitentData)-2,1]) < self.tol:
			print("The last two entries are:" , self.intermitentData.tail(2))
			return True
