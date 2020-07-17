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
		tol = 1e-12
		niter_success = None
		stepsize = 0.4
		interval = 50
		kwargs = {
		'x0': utils.get_static_x0(20,-5, 10),
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
		'x0': utils.get_static_x0((500,20),-5, 10),
		#'x0': utils.get_random_x0(20,-5, 10),
		'bounds':np.full((20,2), (-5.0, 10.0)),
		'strategy': 'best2exp',
		'maxiter':10,
		#'callback':callback_,
		'popsize':25,
		'tol':1e-10,
		'mutation':0.5,
		'recombination': 0.5,
		'polish': True,
		'atol': 0.1,
		'seed': 20,
		'updating':'immediate',
		#'workers':5
		'workers': 4
		}

	elif args.solver == 'dual_annealing':
		def callback_(x,f,context):
			print("custom callback for dual_annealing")
			logger.info(fmt('info', "Dual Annealing Custom Callback Invoked"))
			return
		kwargs = {
		'x0': utils.get_static_x0(20,-5, 10, 4),
		'bounds':np.full((20,2), (-5.0, 10.0)),
		'tol': 1e-15,
		'initial_temp': 5230,
		'maxiter':1000,
		'restart_temp_ratio':2e-5,
		'visit':2.62,
		'accept':-2.0,
		'maxfun': 10000,
		'no_local_search': False,
		'seed': 20
		}

	elif args.solver == 'nelder-mead':
		def callback_(x):
			print("custom callback for nelder-mead")
			return
		kwargs = {
		'x0': utils.get_static_x0(20,-5, 10),
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
			'adaptive':False
		}

		}

	elif args.solver == 'powell':
		def callback_(x):
			print("custom callback for powell")
			return
		kwargs = {
		'x0': utils.get_static_x0(20,-5, 10),
		'method': 'powell',
		'tol': 1e-10,
		'bounds': np.full((20,2), (-5.0, 10.0)),
		'callback':callback_,
		'maxiter':1000,
		'options': {
			'disp':0,
			'maxfev':10000,
			'return_all':False,
			'xtol':1e-5, 
			'ftol':1e-5
		}
		}

	elif args.solver == 'cobyla':
		def callback_(x):
			print("custom callback for cobyla")
			return
		kwargs = {
		'x0': utils.get_static_x0(20,-5, 10),
		'method': 'cobyla',
		'maxiter':1000000,
		'callback':callback_,
		'options': {
			'disp':0,
			'rhoberg':1.0,
			'catol':1e-5,
			'tol':1e-5
		}

		}

	elif args.solver == 'l-bfgs-b':
		def callback_(x):
			print("custom callback for l-bfgs-b")
			return
		kwargs = {
		'x0': utils.get_static_x0(20,-5, 10),
		'method': 'l-bfgs-b',
		'jac':None,
		'bounds': np.full((20,2), (-5.0, 10.0)),
		'maxiter':10000,
		'callback':callback_,
		'options': {
			'disp':0,
			'maxcor':100,
			'ftol':1e-11,
			'gtol':1e-15,
			'eps':0.1,
			'maxfun':10000,
			'maxls':10,
			'finite_diff_rel_step':None
		}

		}

	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		'x0': utils.get_static_x0((400,21), -5, 10),
		'dimensions':21,
		'bounds': np.full((21,2), (-5, 10)),
		'maxiter':3500,
		'n_particles':400,
		'options': {'c1':0.5,'c2': 0.7, 'w' : 0.9},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : None,
						'ftol_iter':2,
						'vh_strategy' : 'unmodified',
						'center' : 1.0,
						'ftol' : 1e-1
						}
		}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RosenbrockDigitalTwin(), args, kwargs)
	else:
		print(cfg.main(RosenbrockDigitalTwin(), args, kwargs))