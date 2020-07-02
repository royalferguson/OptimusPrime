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
<<<<<<< HEAD
			'maxiter':1000,
			'polish' : False,
			'tol' : 0
=======
			'maxiter':10,
			'tol' : 0,
			'polish': False
>>>>>>> f1d4214080c02a3b53c56163ed4edefefc398d89
		}

	def test_default_call_count(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
<<<<<<< HEAD
		self.assertTrue(res.nit <= 1000)
		# Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 160160
		# 1001 * 20 * 8 = 160160
		self.assertTrue(self.obj_func_call_count <=160160)

=======
		self.assertTrue(res.nit <= 10)
		# Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 120120
		self.assertTrue(self.obj_func_call_count <=1760)
		print(self.obj_func_call_count)
>>>>>>> f1d4214080c02a3b53c56163ed4edefefc398d89
	def test_limited_call_count(self):
		self.kwargs['maxiter'] = 1
		res = self.UUT.solve(self.obj_func,**self.kwargs)
		self.assertTrue(res.nit, 1)
<<<<<<< HEAD
		#  Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 320
		# 2 * 20 * 8 = 320
=======
		#  Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 240
>>>>>>> f1d4214080c02a3b53c56163ed4edefefc398d89
		self.assertEqual(self.obj_func_call_count, 320)

	def test_solver_callback(self):
		self.kwargs['maxiter'] = 15
		self.UUT.solve(self.obj_func, **self.kwargs)
		#  Maximum Number of function evaluations (no polishing) is (maxiter + 1) * popsize * len(x) = 320
		# 16 * 20 * 8 = 2560
		self.assertTrue(self.UUT.callback_count <= 2560)

	def test_solver_return(self):
		res = self.UUT.solve(self.obj_func, **self.kwargs)
		self.assertIsInstance(res, OptimizeResult)

if __name__ == '__main__':
	unittest.main()
