import unittest
from OptimusPrime.utils.functions.single_obj import *
import numpy as np 
import math

class TestSingleObjectiveFunctions(unittest.TestCase):

		def test_rosenbrock(self):
			# Non Optimal Solution
			x0 = [1.3, 0.7, 0.8, 1.9, 1.2, 8.3, 2.2, 0.3]
			res = rosenbrock(x0)
			self.assertTrue(isinstance(res, float) )
			self.assetNotEqual(res, 0.0)

			# Optimal Solution
			x0 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
			res = rosenbrock(x0)
			self.assertEqual(res.,0.0)
			

