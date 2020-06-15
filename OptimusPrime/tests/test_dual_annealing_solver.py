import unittest
from OptimusPrime.solvers import DualAnnealingSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
import numpy as np
from numpy import cos, sin
import pprint
import copy


class TestDualAnnealingSolverMethods(unittest.TestCase):
	'''
	Individual Tests are defined with methods whose names begin with test.
	Informs test runner which methods represent test which need to be executed.
	'''

	def stub_obj_func(self,x):
		r = rosenbrock(x)
		self.obj_func_call_count += 1
		return r

	class DualAnnealingSolverTestHelper(DualAnnealingSolver):
		def __init__(self):
			super().__init__()
			self.callback_count=0

		def callback(self,xk, f, accept):
			super().log_data(xk, f, accept)
			self.callback_count += 1


	def setUp(self):
		self.UUT = self.DualAnnealingSolverTestHelper()
		self.kwargs = {
			'x0': np.zeros(8),
			'bounds': np.full((8,2),(-10, 10))

		}
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0
		self.seed = np.random.seed(1234)

	def test_default_call_count(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
		self.assertEqual(res.nit, 1000)   
		self.assertTrue(self.obj_func_call_count >= 0)

	def test_limited_call_count(self):
		kwargs = copy.deepcopy(self.kwargs)
		kwargs['maxiter'] = 1
		res = self.UUT.solve(self.obj_func, **kwargs)
		self.assertTrue(res.nit, 1)
		# NO guaranteee to the number of evaluation calls
		self.assertTrue(self.obj_func_call_count >= 0)

	def test_callback(self):
		kwargs = copy.deepcopy(self.kwargs)
		kwargs['maxiter'] = 3
		kwargs['callback'] = self.UUT.callback
		self.UUT.solve(self.obj_func, **kwargs)
		self.assertTrue(self.UUT.callback_count >= 1) # callback count should be at least 1, it is called for every minima found

	def test_solution(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
		for i in range(8):
			self.assertAlmostEqual(res.x[i],1,3)

	def test_limited_function_evaluations(self):
		kwargs = copy.deepcopy(self.kwargs)
		kwargs['maxfun'] = 100
		res = self.UUT.solve(self.obj_func,**kwargs)
		self.assertTrue(res.nfev, 100)

	

if __name__ == '__main__':
	unittest.main()
