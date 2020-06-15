from OptimusPrime.solvers import BaseSolver
from scipy.optimize import basinhopping
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 
import pandas as pd

class BasinhoppingSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.tol = 0
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, niter=1000, **kwargs):
		if 'tol' in kwargs:
			self.tol = kwargs.pop('tol')
		kwargs.update({'niter' : niter})
		kwargs.update({'callback' : self.log_data})
		return basinhopping(fun, **kwargs)

	_='''
	def callback(self, xk, f, accept):
		self.log_intermediate_data(xk, f, accept)
	'''

	def log_data(self, x, f, accept):
		s = pd.Series([x,f], index=['dv','score'])
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)
		if len(self.intermitentData) >= 2 and abs(self.intermitentData.iloc[len(self.intermitentData)-1,1] - self.intermitentData.iloc[len(self.intermitentData)-2,1]) < self.tol:
			print("The last two entries are:" , self.intermitentData.tail(2))
			return True

