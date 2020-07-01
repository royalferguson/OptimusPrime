import unittest
from OptimusPrime.solvers import DifferentialEvolutionSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
from scipy.optimize import OptimizeResult
import numpy as np
from numpy import cos, sin
import pprint
import copy


class TestDifferentialEvolutionSolverMethods(unittest.TestCase):
	'''
	Individual Tests are defined with methods whose names begin with test.
	Informs test runner which methods represent test which need to be executed.
	'''

	def stub_obj_func(self,x):
		r = rosenbrock(x)
		self.obj_func_call_count += 1
		return r

	class DifferentialEvolutionSolverTestHelper(DifferentialEvolutionSolver):
		def __init__(self):
			super().__init__()
			self.callback_count = 0
			self.obj_func_call_count = 0

		def log_data(self,xk, convergence = None):
			self.callback_count += 1

	def setUp(self):
		self.UUT = self.DifferentialEvolutionSolverTestHelper()
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0
		self.x0 = [1.3, 0.7, 0.8, 1.9, 1.3, 8.3, 2.2, 0.3]
		popsize = 20
		self.x0 = np.array([np.array(self.x0) for i in range(popsize*len(self.x0))])
		self.kwargs = {
			'x0' : self.x0,
			'bounds': np.full((8,2),(-10, 10)),
			'popsize' : popsize,
			'maxiter':10,
			'tol' : 0
		}


	def test_default_call_count(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
		self.assertEqual(res.nit, 10)
		# Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 120120
		self.assertTrue(self.obj_func_call_count <=1201)

	def test_limited_call_count(self):
		self.kwargs['maxiter'] = 1
		res = self.UUT.solve(self.obj_func,**self.kwargs)
		self.assertTrue(res.nit, 1)
		#  Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 240
		self.assertEqual(self.obj_func_call_count, 240)

	def test_solver_callback(self):
		self.kwargs['maxiter'] = 15
		self.UUT.solve(self.obj_func, **self.kwargs)
		self.assertTrue(self.UUT.callback_count >= 2000)

	def test_solver_return(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
		self.assertIsInstance(res, OptimizeResult)

if __name__ == '__main__':
	unittest.main()
