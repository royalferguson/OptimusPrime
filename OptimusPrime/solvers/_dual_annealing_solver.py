from OptimusPrime.solvers import BaseSolver
from scipy.optimize import dual_annealing
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 

class DualAnnealingSolver(BaseSolver):
	def __init__(self):
		self.intermitentData=[]
		self.diff=[]
		self.score=[]

	def solve(self, fun, kwargs):
		return dual_annealing(fun, **kwargs)

	def callback(self, xk, f, accept):
		self.log_intermediate_data(xk, f, accept)

	def log_intermediate_data(self, xk, f, accept):
		i = len(self.intermitentData)
		if i > 0:
			self.diff.append(np.absolute(np.array(self.intermitentData)[i-1] - np.array(xk)))
		self.intermitentData.append(xk.tolist())
		self.score.append(f)
