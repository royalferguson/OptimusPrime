import OptimusPrime.configuration as cfg
from OptimusPrime.solvers import BasinhoppingSolver, ParticleSwarmSolver, DifferentialEvolutionSolver
import numpy as np 
import copy

class Optimus():

	solver_dict={
	'basinhopping'  :  BasinhoppingSolver(),
	'GlobalBestPSO'	:  ParticleSwarmSolver(), 
	'differential_evolution' : DifferentialEvolutionSolver()
	}

	def __init__(self):
		self.solver_params_dict = copy.deepcopy(cfg.default_solver_params_dict)
		self.solver_name='basinhopping'
		self.objective_function = None
		self.minimum = False
		#self.x0 = None
		#self.bounds = None

	def set_solver(self, name):
		self.solver_name = name

	def flip_objective_function(self, func):
		def func_wrapper(*args, **kwargs):
			return 1-func(*args, **kwargs)
		return func_wrapper

	def set_objective_function(self, func, flip=False):
		self.objective_function = self.flip_objective_function(func) if flip else func


	def check_minimum(self,name,kwargs):
		if name == 'basinhopping':
			if 'x0' in kwargs:
				self.minimum = True
		elif name == 'differential_evolution':
			if 'bounds' in kwargs:
				self.minimum = True
		elif name == 'GlobalBestPSO':
			if 'bounds' in kwargs or 'x0' in kwargs or 'dimensions' in kwargs:
				self.minimum = True
		return

	def update_solver_params(self, name, kwargs):
		self.check_minimum(name,kwargs)

		if self.minimum == False:
			print("Current parameter dictionary does not have the minimum required parameters")

		self.solver_params_dict[name].update(kwargs)

	def return_solver_params(self,name):
		return self.solver_params_dict[name]

	"""
	def set_starting_point(self, x):
		self.x0 = x
	
	def set_bounds(self, b):
		self.bounds = b
	"""	
	def solve(self):

		if self.minimum == False:
			print("Current parameter dictionary does not have the minimum required parameters, solve returning none")
			return None
		else:
			res = self.solver_dict[self.solver_name].solve(self.objective_function, kwargs=self.solver_params_dict[self.solver_name])
			return res