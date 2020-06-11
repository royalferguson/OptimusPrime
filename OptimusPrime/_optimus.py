import OptimusPrime.configuration as cfg
from OptimusPrime.solvers import BasinhoppingSolver, ParticleSwarmSolver
import numpy as np 
import copy

class Optimus():

	solver_dict={
	'basinhopping'  :  BasinhoppingSolver(),
	'GlobalBestPSO'	:  ParticleSwarmSolver()
	}

	def __init__(self):
		self.solver_params_dict = copy.deepcopy(cfg.default_solver_params_dict)
		self.solver_name='basinhopping'
		self.objective_function = None
		self.x0 = None
		#self.bounds = None

	def set_solver(self, name):
		self.solver_name = name

	def flip_objective_function(self, func):
		def func_wrapper(*args, **kwargs):
			return 1-func(*args, **kwargs)
		return func_wrapper

	def set_objective_function(self, func, flip=False):
		self.objective_function = self.flip_objective_function(func) if flip else func

	def update_solver_params(self, name, kwargs):
		self.solver_params_dict[name].update(kwargs)

	def return_solver_params(self,name):
		return self.solver_params_dict[name]

	def set_starting_point(self, x):
		self.x0 = x

	def set_bounds(self, b):
		self.bounds = b

	def solve(self):
		print("================", self.solver_name)
		print("===============", self.solver_params_dict[self.solver_name])
		res = self.solver_dict[self.solver_name].solve(self.objective_function, x0=self.x0, **self.solver_params_dict[self.solver_name])
		return res