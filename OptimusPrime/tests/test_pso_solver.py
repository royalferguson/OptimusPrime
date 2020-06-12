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
		if self.limit and self.obj_func_call_count == 100:
			return 0
		r = rosenbrock(x)
		self.obj_func_call_count += 1
		return r

	class ParticleSwarmSolverTestHelper(ParticleSwarmSolver):
		def __init__(self):
			super().__init__()
			self.callback_count=0

		def callback(self,xk, f, accept):
			super().callback(xk, f, accept)
			self.callback_count += 1

	def setUp(self):
		self.UUT = self.ParticleSwarmSolverTestHelper()
		self.kwargs = {
			'n_particles': 10,
			'options':{'c1': 0.5, 'c2': 0.3, 'w':0.9},
			'dimensions':2,
			'bounds':np.full((2,2),(-10, 10)),
			'x0': np.full((2,2), (0,0))
		}
		self.obj_func = self.stub_obj_func
		self.obj_func_call_count=0
		self.limit = False

	def test_default_call_count(self):
		self.limit = False
		res = self.UUT.solve(self.obj_func,self.kwargs)
		self.assertTrue(self.obj_func_call_count > 0)

	def test_limited_call_count(self):
		self.obj_func_call_count=0
		self.limit = True
		res = self.UUT.solve(self.obj_func,self.kwargs)
		self.assertTrue(self.obj_func_call_count == 100)


	def test_solution(self):
		self.obj_func_call_count=0
		self.limit = False
		res = self.UUT.solve(self.obj_func,self.kwargs)
		self.assertAlmostEqual(res[0],0,3)

	def test_solution_variables(self):
		self.obj_func_call_count=0
		self.limit = False
		res = self.UUT.solve(self.obj_func,self.kwargs)
		self.assertAlmostEqual(res[1][0],1,3)
		self.assertAlmostEqual(res[1][1],1,3)

if __name__ == '__main__':
	unittest.main()