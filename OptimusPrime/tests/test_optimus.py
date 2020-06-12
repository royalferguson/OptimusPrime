import unittest
from OptimusPrime import Optimus
from OptimusPrime.solvers import BaseSolver
import OptimusPrime.configuration as cfg
import numpy as np 


class TestOptimusMethods(unittest.TestCase):
	'''
	Individual Tests are defined with methods whose names begin with test.
	Informs test runner which methods represent test which need to be executed.
	'''

	def stub_obj_func(self,x):
		return 1.0

	def setUp(self):
		self.UUT = Optimus()

	def test_solver_dict(self):
		expected = ('nelder-mead','l-bfgs-b', 'powell', 'cobyla', 'basinhopping', 'GlobalBestPSO', 'dual_annealing', 'differential_evolution')
		self.assertTrue (all(name in self.UUT.solver_dict for name in expected))

		# verify dictionary contains solver objects
		for key, solver in self.UUT.solver_dict.items():
			self.assertIsInstance(solver, BaseSolver)
			solve_op = getattr(solver, "solve", None)
			self.assertTrue(callable(solve_op))

	def test_configure_solver_params(self):
		# Verify that changing the optimus parameter dictionary doesn't change the default dictionary
		self.assertTrue(self.UUT.solver_params_dict.get('GlobalBestPSO') == cfg.default_solver_params_dict.get('GlobalBestPSO'))
		self.UUT.update_solver_params('GlobalBestPSO', {'dimensions': 2 ,'maxiter' : 20000, 'n_particles' : 100, 'options' : {'c1': 1.4, 'c2': 2.0, 'w' : 0.9}} )
		self.assertFalse(self.UUT.solver_params_dict.get('GlobalBestPSO') == cfg.default_solver_params_dict.get('GlobalBestPSO'))

	def test_flipping_objective_function(self):
		self.UUT.set_objective_function(self.stub_obj_func, flip = True)
		self.assertEqual(self.UUT.objective_function([]), 0.0)
		


if __name__ == '__main__':
	unittest.main()