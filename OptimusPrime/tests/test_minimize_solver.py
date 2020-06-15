import unittest
from OptimusPrime.solvers import MinimizeSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
import numpy as np 
import copy

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
			self.callback_count = 0


		def callback_(self,xk):
			super().callback_(xk)
			self.callback_count += 1

	def setUp(self):
		self.UUT = self.MinimizeSolverTestHelper()
		self.kwargs = {
			'method': 'l-bfgs-b',
			'tol':1e-7,
			'bounds':np.full((100,2),(-10, 10)), # will only work with some of them
			'x0': np.full(100,0)
		}
		self.callback_count=0
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0

	def test_solver_callback(self):
		kwargs = copy.deepcopy(self.kwargs)
		kwargs['options'] = {'maxiter':1}
		kwargs['callback'] = self.UUT.callback_
		res = self.UUT.solve(self.obj_func,**kwargs)
		self.assertTrue(self.UUT.callback_count > 0)