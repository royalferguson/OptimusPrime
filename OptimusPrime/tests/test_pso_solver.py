import unittest
from OptimusPrime.solvers import ParticleSwarmSolver
from OptimusPrime.utils.functions.single_obj import rosenbrock
import numpy as np 


class TestParticleSwarmSolverMethods(unittest.TestCase):
	'''
	Individual Tests are defined with methods whose names begin with test.
	Informs test runner which methods represent test which need to be executed.
	'''

	def stub_obj_func(self,x):
		r = rosenbrock(x)
		self.obj_func_call_count += 1
		return r

	class ParticleSwarmSolverTestHelper(BasinhoppingSolver):
		def __init__(self):
			super().__init__()
			self.callback_count=0

		def callback(self,xk, f, accept)
			super().callback(xk, f, accept)
			self.callback_count += 1

	def setUp(self):
		self.UUT = self.ParticleSwarmSolverTestHelper()
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0
		self.x0 = [1.3, 0.7, 0.8, 1.9, 1.2, 8.3, 2.2, 0.3]
		self.bnds = np.full((8,2),(-10, 10))

	def test_default_call_count(self):
		res = self.UUT.solve(self.obj_func, x0=self.x0, bounds=self.bnds)
		self.assetEqual(res.nit, 100)   # default number of iterations is 100
		#  No guarantee to the number of function calls
		self.assertEqual(self.obj_func_call_count, 10000)

	def test_limited_call_count(self):
		res = self.UUT.solve(self.obj_func, x0=self.x0, bounds = self.bnds, maxiter=2, n_particles = 10 )
		self.assertEqual(res.obj_func_call_count, 20)


	def test_solver_callback(self):
		res = self.UUT.solve(self.obj_func, x0=self.x0, bounds = self.bnds, maxiter=2, n_particles = 10 )
		self.assertEqual(res.obj_func_call_count, 20)


if __name__ == '__main__':
	unittest.main()