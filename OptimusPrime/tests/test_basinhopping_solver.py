import unittest
from OptimusPrime.solvers import BasinhoppingSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
import numpy as np
from numpy import cos, sin
import pprint
import copy
from scipy.optimize._basinhopping import (RandomDisplacement)


def func2d_nograd(x):
    f = cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] + 0.2) * x[0]
    return f


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

		def callback(self,xk, f, accept):
			super().log_data(xk, f, accept)



	def setUp(self):
		self.UUT = self.BasinhoppingSolverTestHelper()
		self.kwargs = {
			'x0': [1.0, 1.0],
			'niter':100,
			'minimizer_kwargs':{'method': 'L-BFGS-B'}
		}
		self.obj_func = func2d_nograd
		self.obj_func_call_count=0
		self.bnds = np.full((2,2),(-10, 10))
		self.seed = np.random.seed(1234)

	def test_default_call_count(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
		self.assertEqual(res.nit, 100)   
		self.assertTrue(self.obj_func_call_count >= 0)

	def test_limited_call_count(self):

		kwargs = copy.deepcopy(self.kwargs)
		kwargs['niter'] = 1
		kwargs['minimizer_kwargs'].update({'method': 'L-BFGS-B', 'options':{'maxfun' : 15, 'maxiter' : 1}, 'bounds': self.bnds})

		res = self.UUT.solve(self.obj_func,**kwargs)
		self.assertTrue(res.nit, 1)
		# NO guaranteee to the number of evaluation calls
		self.assertTrue(self.obj_func_call_count >= 0)

	def test_callback(self):

		kwargs = copy.deepcopy(self.kwargs)
		kwargs['niter'] = 3
		kwargs['minimizer_kwargs'].update({'method': 'L-BFGS-B', 'options':{'maxfun' : 60, 'maxiter' : 1}, 'bounds': self.bnds})
		kwargs['callback'] = self.UUT.callback
		self.UUT.solve(self.obj_func, **kwargs)
		self.assertTrue(self.UUT.callback_count > 0) # callback count should equal the number of basinhopping iterations

	def test_solution(self):
		kwargs = copy.deepcopy(self.kwargs)
		res = self.UUT.solve(self.obj_func, **kwargs)
		self.assertAlmostEqual(res.x[0], -0.195, 3)
		self.assertAlmostEqual(res.x[1], -0.1, 3)

	def test_accept(self):
		class AcceptTest():
			def __init__(self):
				self.been_called = 0
			def __call__(self,**kwargs):
				self.been_called = 1
				return True

		accept_test = AcceptTest()
		kwargs = copy.deepcopy(self.kwargs)
		kwargs['accept_test'] = accept_test
		self.UUT.solve(self.obj_func, **kwargs)
		self.assertTrue(accept_test.been_called)


if __name__ == '__main__':
	unittest.main()
