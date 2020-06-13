import unittest
from OptimusPrime.solvers import MinimizeSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
import numpy as np 


class MinimizeSolverMethods(unittest.TestCase):
	'''
	Individual Tests are defined with methods whose names begin with test.
	Informs test runner which methods represent test which need to be executed.
	'''

	def stub_obj_func(self,x):
		r = rosenbrock(x)
		self.obj_func_call_count += 1
		return r

	class MinimizeSolverTestHelper(MinimizeSolver):
		def __init__(self):
			super().__init__()


		def callback(self,xk,f):
			super().callback(xk, f, accept)
			self.callback_count += 1

	def setUp(self):
		self.UUT = self.MinimizeSolverTestHelper()
		self.kwargs = {
			'n_particles': 10,
			'options':{'c1': 0.5, 'c2': 0.3, 'w':0.9},
			'dimensions':2,
			'bounds':np.full((2,2),(-10, 10)),
			'x0': np.full((2,2), (0,0))
		}
		self.callback_count=0
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0

	def test_solver_callback(self):
		self.kwargs['callback'] = self.UUT.callback_