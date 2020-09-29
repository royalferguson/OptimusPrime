from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin
import OptimusPrime.configuration as cfg
from OptimusPrime.logger import *
import numpy as np 
import pandas as pd
import argparse, sys
import os

'''
	This twin solves for the rastrigin objective function.

    Rastrigin Function
    non-linear, multi-modal, many local minima
    global minimum: f(x=0,x2=0,....xn=0) = 0
    bounds: -5.12 <= Xi <= 5.12
'''


class RastriginDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):

			# Use this when you wish to provide the initial position (x0)
			super().__init__(rastrigin)

			# Use this when you don't want to provide initial position (x0) - PSO ONLY-
			# super().__init__(rastrigin)

		def optimize(self, args, kwargs):
			return super().optimize(args, kwargs)

if __name__ == '__main__':
	args = cfg.get_commandline_args()

	RDT = RastriginDigitalTwin()

	if args.trace:
		print(utils.run_with_callgraph(cfg.optimizeAll, RastriginDigitalTwin()))
	else:
		cfg.optimizeAll(RastriginDigitalTwin())

