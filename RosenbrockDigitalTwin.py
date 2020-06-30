from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rosenbrock
import OptimusPrime.configuration as cfg
from OptimusPrime.logger import *
import numpy as np 
import pandas as pd
import argparse, sys
import os

class RosenbrockDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):

			super().__init__(rosenbrock)


		def optimize(self, args, kwargs):
			return super().optimize(args, kwargs)

if __name__ == '__main__':
	args = cfg.get_commandline_args()
	if os.path.exists('optimization_data.pkl'):
		os.remove('optimization_data.pkl')
	# for basinhopping
	if args.solver == 'basinhopping':
		def callback_(x,f,accept):
			print("custom callback for basinhopping")
			logger.info(fmt('info', "Basinhopping Custom Callback Invoked"))
			return
		T = 1.0
		niter = 1000
		tol = 1e-5
		niter_success = None
		stepsize = 0.5
		interval = 50
		kwargs = {
		'x0': utils.get_random_x0(50,-5, 10),
		'niter':niter,
		'T': T,
		'stepsize':stepsize,
		'minimizer_kwargs': {
			'method':'BFGS'
		},
		'interval':interval,
		'disp':0,
		'tol': tol,
		'niter_success':niter_success,
		'accept_test': None,
		'take_step': None,
		'seed': 20
		}
	elif args.solver == 'differential_evolution':
		def callback_(x,convergence=2):
			print("custom callback for differential_evolution")
			logger.info(fmt('info', "Differential Evolution Custom Callback Invoked"))
			return
		kwargs = {
		'x0': utils.get_random_x0((20,10),-5, 10),
		'bounds':np.full((20,2), (-5.0, 10.0)),
		'strategy': 'best2exp',
		'maxiter':10,
		#'callback':callback_,
		'popsize':10,
		'tol':1e-10,
		'mutation':1.5,
		'recombination': 0.5,
		'polish': True,
		'atol': 0.1,
		'seed': 20,
		'updating':'immediate',
		#'workers':5
		'workers': 1
		}

	elif args.solver == 'dual_annealing':
		def callback_(x,f,context):
			print("custom callback for dual_annealing")
			logger.info(fmt('info', "Dual Annealing Custom Callback Invoked"))
			return
		kwargs = {
		'x0': utils.get_random_x0(50,-5, 10),
		'bounds':np.full((50,2), (-5.0, 10.0)),
		'tol': 1e-15,
		'initial_temp': 0.5,
		'maxiter':1000,
		'restart_temp_ratio':0.5,
		'visit':2,
		'accept':-6.0,
		'maxfun': 10000,
		'no_local_search': False,
		'seed': 20
		}

	elif args.solver == 'nelder-mead':
		def callback_(x):
			print("custom callback for nelder-mead")
			return
		kwargs = {
		'x0': utils.get_random_x0(50,-5, 10),
		'method': 'nelder-mead',
		'tol': 1e-15,
		'callback':callback_,
		'maxiter':100000,
		'options': {
			'disp':0,
			'maxfev':None,
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
		'x0': utils.get_random_x0(50,-5, 10),
		'method': 'powell',
		'tol': 1e-15,
		'bounds': np.full((50,2), (-5.0, 10.0)),
		'callback':callback_,
		'maxiter':1000,
		'options': {
			'disp':0,
			'maxfev':10000,
			'return_all':False,
			'xtol':1e-15, 
			'ftol':1e-15
		}
		}

	elif args.solver == 'cobyla':
		def callback_(x):
			print("custom callback for cobyla")
			return
		kwargs = {
		'x0': utils.get_random_x0(50,-5, 10),
		'method': 'cobyla',
		'maxiter':1000000,
		'callback':callback_,
		'options': {
			'disp':0,
			'rhoberg':1.0,
			'catol':1e-15,
			'tol':1e-15
		}

		}

	elif args.solver == 'l-bfgs-b':
		def callback_(x):
			print("custom callback for l-bfgs-b")
			return
		kwargs = {
		'x0': utils.get_random_x0(50,-5, 10),
		'method': 'l-bfgs-b',
		'jac':None,
		'bounds': np.full((50,2), (-5.0, 10.0)),
		'maxiter':10000,
		'callback':callback_,
		'options': {
			'disp':0,
			'maxcor':100,
			'ftol':1e-15,
			'gtol':1e-15,
			'eps':0.1,
			'maxfun':10000,
			'maxls':10,
			'finite_diff_rel_step':None
		}

		}
	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		'x0': utils.get_random_x0((20,100), -5, 10),
		'dimensions':20,
		'bounds': np.full((20,2), (-5, 10)),
		'maxiter':3000,
		'tol' : 0.1,
		'n_particles':100,

		'options': {'c1':0.2,'c2': 0.6, 'w' : 0.95},
		'pso_kwargs': {'bh_strategy' : 'random',	# random or periodic
						'velocity_clamp' : None,
						'vh_strategy' : 'unmodified',
						'center' : 2,
						'ftol' : -np.inf
						}
		}


	if args.trace:
		utils.run_with_callgraph(cfg.main, RosenbrockDigitalTwin(), args, kwargs)
	else:
		cfg.main(RosenbrockDigitalTwin(), args, kwargs)


