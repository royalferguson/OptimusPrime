from OptimusPrime.solvers import BaseSolver
import pyswarms as ps
from scipy.optimize import OptimizeResult
import numpy as np 
import pandas as pd
import seaborn as sb 
import matplotlib.pyplot as plt 
from pyswarms.utils.plotters import plot_cost_history, plot_contour, plot_surface
from pyswarms.utils.plotters.formatters import Mesher, Designer


_='''
pyswarms:  Objective function signature is f(x, **kwargs) -> numpy.ndarray(n_particles)
		   where x is a numpy.ndarray set of inputs shape(n_particles, dimensions).

scipy:     Objective function signature is f(x, *args) -> float
		   where x is 1-d array set of inputs of shape (n,) where n is the dimensions.
'''


class ParticleSwarmSolver(BaseSolver):
	def __init__(self):
		self.tol_hit = False
		self.tol=0
		self.intermitentData = []
		self.n_particles=0
		self.stopped_at = 0
		self.particle_hit=[]

	def pso_objective_function(self, func, log_cb=None, tol_cb=None):

		# means of creating a vectorized matrix - which PSO expects
		#
		def func_wrapper(x, **kwargs):
			j=[]
			stop = False
			particle_num=0
			if tol_cb:
				stop = tol_cb()
			if stop != True:
				for particle_x in x:
					particle_num+=1
					score = func(particle_x)
					if log_cb:
						log_cb(particle_num, particle_x, score)
					j.append(score)
				return np.hstack(j)
			return np.zeros(len(x))
		return func_wrapper
		
	# def pso_global_optimize(self, fun, dimension = None, x0=None, bounds=None, maxiter=1000, n_particles=10, options={'c1':0.2,'c2': 0.6, 'w' : 0.95}, pso_kwargs={}, fun_kwargs={}):
	def pso_global_optimize(self, fun, dimensions = None, x0=None, bounds=None, maxiter=1000, n_particles=10, options={'c1':0.2,'c2': 0.6, 'w' : 0.95}, pso_kwargs={}, fun_kwargs={}):

		# In PSO - you can specify x0, bounds, both, or neither.  If you specify x0
		# and don't specify bounds - then defaults of -10000, 10000 are used
		if bounds is not None:
			bounds = np.transpose(bounds)
		
		if x0 is not None:
			dimensions = len(x0)
		elif bounds is not None:
			dimensions = len(bounds[0])
		elif dimensions is None:
			dimensions = 2
		self.n_particles = n_particles
		# PSO uses multiple particles - each must have a starting point
		# if x0 does not contain one for each particle - then generate a random point for it.
		# 
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
		if x0 is None and bounds is None:
			optimizer = ps.single.GlobalBestPSO(n_particles, dimensions, options, **pso_kwargs)
		else:
			optimizer = ps.single.GlobalBestPSO(n_particles, dimensions, options, bounds=bounds, init_pos=x0, **pso_kwargs)

		
		objective_func = self.pso_objective_function(fun, log_cb=self.log_data, tol_cb=self.tolerance_check)
		best = optimizer.optimize(objective_func, maxiter, **fun_kwargs)
		if self.stopped_at != 0:
			print("Stopped early at position: ", self.stopped_at)
			print("last 2*n_particle solutions")
			for i in range(self.n_particles):
				print(self.intermitentData[-(i+1)], self.intermitentData[-(i+1)-n_particles])
		return best

	def solve(self, fun, **kwargs):
		if 'tol' in kwargs:
			self.tol = kwargs.pop('tol')

		self.n_particles = kwargs['n_particles']
		return self.pso_global_optimize(fun, **kwargs)

	# Q  Why not  solve(self, *args, kwargs)
	#                  return(self.pso_global_optimize(*args, **kwargs))


	def log_data(self, particle_num, particle, f):
		self.intermitentData.append([particle_num,particle,f])
		self.log_data_to_pickle(particle_num, particle, f)

	def log_data_to_pickle(self, particle_num, x, f):
		pass

	def tolerance_check(self):
		if len(self.intermitentData) >= 2 * self.n_particles and self.tol is not None and self.tol_hit is False:
			for x in range(1, self.n_particles + 1):
				current_particle = self.intermitentData[-x][2]
				last_particle = self.intermitentData[-x-self.n_particles][2]
				if abs(current_particle-last_particle) > self.tol:
					return False
			self.stopped_at = len(self.intermitentData)/self.n_particles
			self.tol_hit = True
			return True
		else:
			if self.tol_hit == True:
				return True
			return False

