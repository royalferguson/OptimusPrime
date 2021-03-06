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
	if os.path.exists('optimization_data.pkl'):
		os.remove('optimization_data.pkl')
	# for basinhopping
	if args.solver == 'basinhopping':
		def callback_(x,f,accept):
			print("custom callback for basinhopping")
			logger.info(fmt('info', "Basinhopping Custom Callback Invoked"))
			return
		T = 1.0
		niter = 200
		tol = 1e-12
		niter_success = None
		stepsize = 0.5
		interval = 50
		kwargs = {
		'x0': utils.get_random_x0(20,-5.12,5.12),
		'niter':niter,
		'T': T,
		'stepsize':stepsize,
		'minimizer_kwargs': {
			'method':'powell'
		},
		'tol':tol,
		'interval':interval,
		'disp':0,
		'niter_success':niter_success,
		'accept_test': None,
		'take_step': None
		}
	elif args.solver == 'differential_evolution':
		def callback_(x,convergence=2):
			print("custom callback for differential_evolution")
			logger.info(fmt('info', "Differential Evolution Custom Callback Invoked"))
			return
		kwargs = {
		#  utils.get_random_x0(((popsize * #dv),#dv),min_value,max_value)
		'x0': utils.get_random_x0((20,20),-5.12,5.12),
		'bounds':np.full((20,2), (-5.12, 5.12)),
		'strategy': 'best2exp',
		'maxiter':800,
		#'callback':callback_,
		'popsize':1,
		'tol':1e-10,
		'mutation':0.5,
		'recombination': 0.5,
		'polish': True,
		'atol': 0.1,
		'seed': 20,
		'updating':'immediate',
		#'workers':5
		'workers': -1
		}

	elif args.solver == 'dual_annealing':
		def callback_(x,f,context):
			print("custom callback for dual_annealing")
			logger.info(fmt('info', "Dual Annealing Custom Callback Invoked"))
			return
		kwargs = {
		'x0': utils.get_random_x0(20,-5.12, 5.12),
		'bounds':np.full((20,2), (-5.12, 5.12)),
		'tol': 1e-15,
		'initial_temp': 5230,
		'maxiter':2000,
		'restart_temp_ratio':2e-5,
		'visit':2.62,
		'accept':-2.0,
		'maxfun': 15000,
		'no_local_search': False,
		'seed': 20
		}

	elif args.solver == 'nelder-mead':
		def callback_(x):
			print("custom callback for nelder-mead")
			return
		kwargs = {
		'x0': utils.get_random_x0(20, -5.0,5.0),
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
		'x0': utils.get_random_x0(20, -5.0,5.0),
		'method': 'powell',
		'tol': 1e-10,
		'bounds': np.full((20,2), (-5.0, 5.0)),
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
		'x0': utils.get_random_x0(20,-5.0,5.0),
		'method': 'cobyla',
		'maxiter':1000000,
		'options': {
			'disp':0,
			'tol':1e-15,
			'catol':1e-15
		}

		}

	elif args.solver == 'l-bfgs-b':
		def callback_(x):
			print("custom callback for l-bfgs-b")
			return
		kwargs = {
		'x0': utils.get_random_x0(20, -5.0,5.0),
		'method': 'l-bfgs-b',
		'jac':None,
		'bounds': np.full((20,2), (-5.0, 5.0)),
		'maxiter':10000,
		'callback':callback_,
		'options': {
			'disp':0,
			'maxcor':100,
			'ftol':1e-15,
			'gtol':1e-15,
			'eps':1,
			'maxfun':10000,
			'maxls':10,
			'finite_diff_rel_step':None
		}

		}
	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		# 'x0': utils.get_random_x0((300,20), -5.12, 5.12),
		'x0': utils.get_static_x0((300,20), -5.12, 5.12, seed=3.0),
		'dimensions':20,
		'bounds': np.full((20,2), (-5.12,5.12)),
		'maxiter': 3000,   #2750
		'n_particles':300,

		'options': {'c1':0.3,'c2': 0.65, 'w' : 0.95},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : None,
						'vh_strategy' : 'unmodified',
						'center' : 1.0,
						'ftol' : 1e-15,
						'ftol_iter' : 3
						}
		}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args, kwargs)
	else:
		cfg.main(RastriginDigitalTwin(), args, kwargs)


