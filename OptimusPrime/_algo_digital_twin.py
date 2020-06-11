from OptimusPrime import Optimus

class AlgoDigitalTwin():
	#def __init__(self, of, flip=False, x0=None, bounds=None):
	def __init__(self, of, flip=False):
		self.optimizer = Optimus()
		self.algo_objective_func = of
		self.flip = flip
		#self.x0 = x0
		#self.bounds = bounds

	def optimize(self, args, kwargs):
		self.optimizer.set_objective_function(self.algo_objective_func, self.flip)
		#self.optimizer.set_starting_point(self.x0)
		#self.optimizer.set_bounds(self.bounds)
		self.optimizer.set_solver(args.solver)
		self.optimizer.update_solver_params(args.solver, kwargs)

		print("In AlgoDigitalTwin: ")
		for key, value in kwargs.items():
			print("%s == %s" % (key,value) )

		print("kwargs: ", kwargs)

		return self.optimizer.solve()

