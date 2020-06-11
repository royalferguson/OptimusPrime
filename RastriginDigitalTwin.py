from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin
import OptimusPrime.configuration as cfg
import numpy as np 
import argparse, sys

class RastriginDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):

			# Use this when you wish to provide the initial position (x0)
			super().__init__(rastrigin, x0 = utils.get_random_x0(10,-5.12, 5.12))

			# Use this when you don't want to provide initial position (x0) - PSO ONLY-
			# super().__init__(rastrigin)

		def optimize(self, args, kwargs):
			return super().optimize(args, kwargs)

if __name__ == '__main__':
	args = cfg.get_commandline_args()

	# for basinhopping
	if args.solver == 'basinhopping':

		def callback_(x,f,accept):
			print("custom callback for basinhopping")
			return

		kwargs = {
		'niter':2,
		'T': 0.2,
		'stepsize':0.65,
		'minimizer_kwargs': {
			'method':'BFGS'
		},
		'interval':2,
		'disp':1,
		'niter_success':2,
		'accept_test': None,
		'take_step': None,
		'callback': callback_,
		'seed': 20
		}

	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		'dimensions':10,
		'bounds': np.full((10,2), (-5.12, 5.12)),
		'maxiter':100,
		'n_particles':200,
		'options': {'c1':0.5,'c2': 0.7, 'w' : 0.85},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : (1,2),
						'vh_strategy' : 'unmodified',
						'center' : 2,
						'ftol' : -1
						}
		}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args, kwargs)
	else:
		cfg.main(RastriginDigitalTwin(), args, kwargs)


