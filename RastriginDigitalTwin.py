from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin
import OptimusPrime.configuration as cfg
import numpy as np 
import argparse, sys

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

	# for basinhopping
	if args.solver == 'basinhopping':

		def callback_(x,f,accept):
			print("custom callback for basinhopping")
			return

		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'niter':2,
		'T': 0.2,
		'stepsize':0.65,
		'minimizer_kwargs': {
			'method':'BFGS'
		},
		'interval':2,
		'disp':1,
		'tol': 10,
		'niter_success':2,
		'accept_test': None,
		'take_step': None,
		'seed': 20
		}

	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		'x0': utils.get_random_x0(2,-5.12, 5.12),
		'dimensions':2,
		'bounds': np.full((2,2), (-5.12, 5.12)),
		'maxiter':50000,
		'tol' : 0.1,
		'n_particles':2,

		'options': {'c1':0.5,'c2': 0.7, 'w' : 0.85},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : (1,2),
						'vh_strategy' : 'unmodified',
						'center' : 2,
						'ftol' : -1
						}
		}
	elif args.solver == 'differential_evolution':
		def callback_(x,convergence=2):
			print("custom callback for differential_evolution")
			return
		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'bounds':np.full((10,2), (-5.12, 5.12)),
		'strategy': 'best2exp',
		'maxiter':5,
		'callback':callback_,
		'popsize':10,
		'tol':1e-10,
		'mutation':1.5,
		'recombination': 0.5,
		'polish': True,
		'atol': 0.1,
		'seed': 20,
		'updating':'immediate',
		'workers':5
		}

	elif args.solver == 'dual_annealing':
		def callback_(x,f,context):
			print("custom callback for dual_annealing")
			return
		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'bounds':np.full((10,2), (-5.12, 5.12)),
		'tol': 10,
		'initial_temp': 0.5,
		'maxiter':5,
		'restart_temp_ratio':0.5,
		'visit':2,
		'accept':-6.0,
		'maxfun': 1000,
		'no_local_search': False,
		'seed': 20
		}

	elif args.solver == 'nelder-mead':
		def callback_(x):
			print("custom callback for nelder-mead")
			return
		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'method': 'nelder-mead',
		'tol': 0.1,
		'callback':callback_,
		'options': {
			'disp':0,
			'maxiter':2,
			'maxfev':1000,
			'return_all':False,
			'xatol':0.1, # Currently doesn't work
			'fatol':0.1, # Currently doesn't work
			'adaptive':True
		}

		}

	elif args.solver == 'powell':
		def callback_(x):
			print("custom callback for powell")
			return
		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'method': 'powell',
		'tol': 0.1,
		'bounds': np.full((10,2), (-5.12, 5.12)),
		'callback':callback_,
		'options': {
			'disp':0,
			'maxiter':2,
			'maxfev':1000,
			'return_all':False,
			'xtol':0.1, 
			'ftol':0.1
		}

		}

	elif args.solver == 'cobyla':
		def callback_(x):
			print("custom callback for cobyla")
			return
		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'method': 'cobyla',
		'callback':callback_,
		'options': {
			'disp':0,
			'maxiter':1000,
			'rhoberg':2,
			'catol':0.0001,
			'tol':0.0001
		}

		}

	elif args.solver == 'l-bfgs-b':
		def callback_(x):
			print("custom callback for l-bfgs-b")
			return
		kwargs = {
		'x0': utils.get_random_x0(10,-5.12, 5.12),
		'method': 'l-bfgs-b',
		'jac':None,
		'bounds': np.full((10,2), (-5.12, 5.12)),
		'callback':callback_,
		'options': {
			'disp':0,
			'maxcor':100,
			'ftol':0.0001,
			'gtol':0.0001,
			'eps':0.1,
			'maxfun':1000,
			'maxiter':2,
			'maxls':10,
			'finite_diff_rel_step':None
		}

		}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args, kwargs)
	else:
		cfg.main(RastriginDigitalTwin(), args, kwargs)


