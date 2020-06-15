from OptimusPrime.solvers import BaseSolver
from scipy.optimize import basinhopping
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 
import pandas as pd

class BasinhoppingSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, niter=1000, **kwargs):
		kwargs.update({'niter' : niter})
		if 'callback' not in kwargs:
			kwargs.update({'callback' : self.log_data})
		return basinhopping(fun, **kwargs)

	_='''
	def callback(self, xk, f, accept):
		self.log_intermediate_data(xk, f, accept)
	'''

	def log_data(self, x, f, accept):
		s = pd.Series([x,f], index=['dv','score'])
		print("===========================================", s)
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)
