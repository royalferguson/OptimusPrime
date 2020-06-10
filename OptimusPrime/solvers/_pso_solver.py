from OptimusPrime.solvers import BaseSolver
import pyswarms as ps
from scipy.optimize import OptimizeResult
import numpy as np 
import seaborn as sb 
import matplotlib.pyplot as plt 
from pyswarms.utils.plotters import plot_cost_history, plot_contour, plot_surface
from pyswarms.utils.plotters.formatters import Mesher, Designer

_='''
pyswarms:  Objective function signature is f(x, **kwargs) -> nummpy.ndarray(n_particles)
		   where x is a numpy.ndarray set of inputs shape(n_particles, dimensions).

scipy:     Objective function signature is f(x, *args) -> float
		   where x is 1-d array set of inputs of shape (n,) where n is the dimensions.
'''

def pso_objective_function(func, log_cb=None, tol_cb=None):

	# means of creating a vectorized matrix - which PSO expects
	#
	def func_wrapper(x, **kwargs):
		j=[]
		stop = False
		if tol_cb:
			stop = tol_cb()
		if stop is not True:
			for particle_x in x:
				score = func(particle_x)
				if log_cb:
					log_cb(particle_x, score)
				j.append(score)
		return np.hstack(j)
	return func_wrapper

class ParticleSwarmSolver(BaseSolver):
	def __init__(self):
		self.tol_hit = False

	def pso_global_optimize(self, fun, dimensions = None, x0=None, bounds=None, maxiter=1000, n_particles=10, options={'c1':0.2,'c2': 0.6, 'w' : 0.95}, pso_kwargs={}, fun_kwargs={}):

		if bounds is not None:
			bounds = np.transpose(bounds)
		
		if x0 is not None:
			dimensions = len(x0)
		elif bounds is not None:
			dimensions = len(bounds[0])
		else:
			dimensions = 2

		# PSO uses multiple particles - each must have a starting point
		# if x0 does not contain one for each particle - then generate a random point for it.
		if x0 is not None:
			x0 = np.asarray(x0)
			if x0.ndim == 1 or x0.shape[1] != n_particles:
				diff = n_particles - x0.ndim
				if bounds is not None:
					r = np.random.uniform(bounds[0][0], bounds[1][0], (diff, dimensions))
				else:
					r = np.random.uniform(-10000, 10000, (diff, dimensions))
					bounds = np.transpose(np.full((dimensions,2), (-10000, 10000)))
				x0 = np.vstack( (x0,r))
		res= {}
		print("bounds: ", bounds)
		print("x0: ", x0)
		print("dimensions: ", dimensions)
		if x0 is None and bounds is None:
			optimizer = ps.single.GlobalBestPSO(n_particles, dimensions, options, **pso_kwargs)
		else:
			optimizer = ps.single.GlobalBestPSO(n_particles, dimensions, options, bounds=bounds, init_pos=x0, **pso_kwargs)
		
		objective_func = pso_objective_function(fun, log_cb=self.log_data, tol_cb=self.tolerance_check)
		best = optimizer.optimize(objective_func, maxiter, **fun_kwargs)
		print(best)
		return best

	def solve(self, fun, x0, **kwargs):
		return self.pso_global_optimize(fun, x0 = x0, **kwargs)

	def log_data(self, xk, f):
		self.log_data_to_pickle(xk,f)

	def log_data_to_pickle(self, xk, f):
		pass

	def tolerance_check(self):
		if self.tol_hit is True:
			return True
		else:
			# add toelrance check logic here
			return False

