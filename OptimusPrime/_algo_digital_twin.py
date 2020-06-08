from OptimusPrime import Optimus

class AlgoDigitalTwin():
	def __init__(self, of, flip=False, x0=None, bounds=None):
		self.optimizer = Optimus()
		self.algo_objective_func = of
		self.flip = flip
		self.x0 = x0
		self.bounds = bounds

	def optimize(self, args, kwargs):
		self.optimizer.set_objective_function(self.algo_objective_func, self.flip)
		self.optimizer.set_starting_point(self.x0)
		self.optimizer.set_bounds(self.bounds)
		self.optimizer.set_solver(args.solver)

		print("In OPTIMUS:  =====================================   kwargs", kwargs)
		
		#[roy]
		# self.optimizer.update_solver_params(args.options)

		#return self.optimizer.solve()
		return 

