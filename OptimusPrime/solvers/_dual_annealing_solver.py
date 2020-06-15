from OptimusPrime.solvers import BaseSolver
from scipy.optimize import dual_annealing
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt
import pandas as pd

class DualAnnealingSolver(BaseSolver):
	def __init__(self):
		super().__init__()
		self.intermitentData = pd.DataFrame()

	def solve(self, fun, maxiter=1000, **kwargs):
		kwargs.update({'maxiter' : maxiter})
		kwargs.update({'callback' : self.log_data})
		return dual_annealing(fun, **kwargs)

	_='''
	def callback(self, xk, f, accept):
		self.log_data(xk, f, accept)
	'''

	def log_data(self, x, f, accept):
		s = pd.Series([x,f], index=['dv','score'])
		self.intermitentData=self.intermitentData.append(s, ignore_index=True)
