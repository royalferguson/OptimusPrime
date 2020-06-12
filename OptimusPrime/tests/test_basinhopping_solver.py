import unittest
from OptimusPrime.solvers import BasinhoppingSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
import numpy as np 
import pprint

class TestBasinhoppingSolverMethods(unittest.TestCase):
	'''
	Individual Tests are defined with methods whose names begin with test.
	Informs test runner which methods represent test which need to be executed.
	'''

	def stub_obj_func(self,x):
		r = rosenbrock(x)
		self.obj_func_call_count += 1
		return r

	class BasinhoppingSolverTestHelper(BasinhoppingSolver):
		def __init__(self):
			super().__init__()
			self.callback_count=0

		def callback(self,xk, f, accept)
			super().callback(xk, f, accept)
			self.callback_count += 1

	def setUp(self):
		self.UUT = self.BasinhoppingSolverTestHelper()
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0
		self.x0 = [1.3, 0.7, 0.8, 1.9, 1.2, 8.3, 2.2, 0.3]
		self.bnds = np.full((8,2),(-10, 10))

	def test_default_call_count(self):
		res = self.UUT.solve(self.obj_func, x0=self.x0, bounds=self.bnds)
		self.assetEqual(res.nit, 100)   # default number of iterations is 100
		#  No guarantee to the number of function calls
		self.assertTrue(self.obj_func_call_count >= 100)

	def test_limited_call_count(self):
		res = self.UUT.solve(self.obj_func, x0=self.x0, bounds = self.bnds, maxiter=1, minimizer_kwargs={'method': 'L-BFGS-B', 'options':{'maxfun' : 15, 'maxiter' : 1}} )
		self.assertTrue(res.nit, 1)
		# NO guaranteee to the number of evaluation calls
		self.assertTrue(self.obj_func_call_count >= 15)

	def test_solver_callback(self):
		self.UUT.solve(self.obj_func, x0=self.x0, bounds=self.bnds, maxiter=3, minimizer_kwargs={'method': 'L-BFGS-B', 'options':{'maxfun' : 60, 'maxiter' : 1}} )
		self.assertEqual(self.UUT.callback_count, 3) # callback count should equal the number of basinhopping iterations


if __name__ == '__main__':
	unittest.main()
