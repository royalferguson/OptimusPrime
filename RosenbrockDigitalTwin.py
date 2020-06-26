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
		intermitentData = pd.DataFrame(columns=['solver','#DV','T', 'stepsize','interval','niter_limit', 'niter_success', 'tol','fun','niter','nfev'])
		Ts = [0.1,0.5,1.5]
		stepsizes = [0.2,0.4,0.6]
		intervals = [35,65,45]
		niter_successes = [1,5,10]
		niters = [100,3000,10000]
		tols = [0.1,1e-5,1e-10]
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
		'x0': [7.49765356,  2.80304508,  8.43095363, -0.99048342,  2.10733416,
        8.3196306 , -0.3348544 ,  5.59323437,  3.38826839,  7.90740441,
        4.2364616 , -2.79102244, -4.80551047, -0.51906156,  2.07349191,
       -1.9777224 ,  3.69346114, -0.14598644, -1.40516507,  2.24830503,
        9.45673335, -3.14701178,  2.98622262,  4.57647219, -0.99854946,
        8.34162379,  9.80291482,  2.44753073,  5.62414469,  5.89917864,
        9.62844113,  7.38993873,  5.32779454,  8.66265065, -1.41528414,
        6.38647093,  0.59250018,  9.80528147,  1.37172202,  7.20986853,
        5.43097582, -0.73761008,  2.18340814,  6.08281799,  8.59424905,
       -1.19962718, -4.30147441, -1.48424773,  0.50599313,  7.08440865],
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
		app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
		
		
	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		'x0': np.full((20,10),0.0),
		'dimensions':20,
		'bounds': np.full((20,2), (-5, 10)),
		'maxiter':1000,
		'n_particles':10,

		'options': {'c1':0.2,'c2': 0.6, 'w' : 0.95},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : None,
						'vh_strategy' : 'unmodified',
						'center' : 1,
						#'ftol' : 0.1
						'ftol' : -np.inf
						}
		}
	elif args.solver == 'differential_evolution':
		def callback_(x,convergence=2):
			print("custom callback for differential_evolution")
			logger.info(fmt('info', "Differential Evolution Custom Callback Invoked"))
			return
		kwargs = {
		'x0': utils.get_random_x0(20,-5, 10),
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

	if args.trace:
		utils.run_with_callgraph(cfg.main, RosenbrockDigitalTwin(), args, kwargs)
	else:
		cfg.main(RosenbrockDigitalTwin(), args, kwargs)


