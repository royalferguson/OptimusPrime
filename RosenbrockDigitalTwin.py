from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rosenbrock
import OptimusPrime.configuration as cfg
from OptimusPrime.logger import *
import numpy as np 
import pandas as pd
import argparse, sys
from OptimusPrime.utils.functions.fileio import *
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
	bounds = readBounds()

	if args.solver == 'basinhopping':
		def callback_(x,f,accept):
			print("custom callback for basinhopping")
			logger.info(fmt('info', "Basinhopping Custom Callback Invoked"))
			return
		startingValues = readFromCsv("basinhopping")
		bounds = bounds.to_numpy()
		if isinstance(startingValues,bool) and startingValues == False:
			x = utils.get_random_multiple_boundaries(bounds, len(bounds))
		else:
			minAt = startingValues['score'].idxmin()
			x = np.fromstring(startingValues.iloc[minAt]['dv'][1:-1], dtype=np.float64, sep=' ') 
		T = 1.0
		niter = 1
		tol = 1e-12
		niter_success = None
		stepsize = 0.4
		interval = 50
		kwargs = {
		'x0': x,
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
		startingValues = readFromCsv("differential_evolution")
		bounds = bounds.to_numpy()
		popsize = 2
		if isinstance(startingValues,bool) and startingValues == False:
			x = utils.get_random_multiple_boundaries(bounds, (popsize*len(bounds), len(bounds)))
		else:
			minAt = startingValues['score'].idxmin()
			x = np.fromstring(startingValues.iloc[minAt]['dv'][1:-1], dtype=np.float64, sep=' ') 
			vals = np.ones((popsize*len(bounds),len(bounds)))
			for i in range(popsize*len(bounds)):
				vals[i] = x
			x = vals
		print(x, bounds)
		kwargs = {
		'x0': x,
		#'x0': utils.get_random_x0(20,-5, 10),
		'bounds': bounds,
		'strategy': 'best2exp',
		'maxiter':1,
		#'callback':callback_,
		'popsize': popsize,
		'tol':1e-10,
		'mutation':0.5,
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
		bounds = bounds.to_numpy()
		startingValues = readFromCsv("dual_annealing")
		if isinstance(startingValues,bool) and startingValues == False:
			x = utils.get_random_multiple_boundaries(bounds, len(bounds))
		else:
			minAt = startingValues['score'].idxmin()
			x = np.fromstring(startingValues.iloc[minAt]['dv'][1:-1], dtype=np.float64, sep=' ') 
		kwargs = {
		'x0': x,
		'bounds': bounds,
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
		'x0': utils.get_random_x0(20,-5, 10),
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
		'x0': utils.get_random_x0(20,-5, 10),
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
		'x0': utils.get_random_x0(20,-5, 10),
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
		'x0': utils.get_random_x0(20,-5, 10),
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
		bounds = bounds.to_numpy()
		n_particles = 400
		startingValues = readFromCsv("GlobalBestPSO")
		if isinstance(startingValues,bool) and startingValues == False:
			x = utils.get_random_multiple_boundaries(bounds, (n_particles,len(bounds)) )
		else:
			minAt = startingValues['score'].idxmin()
			x = np.fromstring(startingValues.iloc[minAt]['dv'][1:-1], dtype=np.float64, sep=' ')
			vals = np.ones((n_particles,len(bounds)))
			for i in range(n_particles):
				vals[i] = x
			x = vals
		for i in range(len(bounds)):
			bounds[i] = (bounds[i][0],bounds[i][1])
		kwargs = {
		'x0': x,
		'dimensions':20,
		'bounds': bounds,
		'maxiter':2,
		'n_particles':n_particles,

		'options': {'c1':0.5,'c2': 0.7, 'w' : 0.9},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : None,
						'vh_strategy' : 'unmodified',
						'center' : 1.0,
						'ftol' : 1e-10
						}
		}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RosenbrockDigitalTwin(), args, kwargs)
	else:
		cfg.main(RosenbrockDigitalTwin(), args, kwargs)
		


