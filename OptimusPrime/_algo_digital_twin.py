from OptimusPrime import Optimus
from OptimusPrime.solvers import default_solver_params_dict

class AlgoDigitalTwin():
	#def __init__(self, of, flip=False, x0=None, bounds=None):
	def __init__(self, of, flip=False):
		self.optimizer = Optimus()
		self.algo_objective_func = of
		self.flip = flip

	def optimize(self, args, kwargs):
		self.optimizer.set_objective_function(self.algo_objective_func, self.flip)
		#self.optimizer.set_starting_point(self.x0)
		#self.optimizer.set_bounds(self.bounds)
		self.optimizer.set_solver(args.solver)
		self.optimizer.update_solver_params(args.solver, kwargs)
		
		return self.optimizer.solve()

	def optimizeAll(self):
		self.optimizer.set_objective_function(self.algo_objective_func, self.flip)
		results = {}
		for key, value in default_solver_params_dict.items():
			print(key)
			self.optimizer.set_solver(key)
			self.optimizer.update_solver_params(key, value)
			results[key] = self.optimizer.solve()
		
		minSolver = ''
		minFun = 99999999999

		for key, value in results.items():
			if value.fun < minFun:
				minSolver = key
				minFun = value.fun

		return minSolver, results[minSolver]
