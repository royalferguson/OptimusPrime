from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin, rosenbrock
import OptimusPrime.configuration as cfg
from OptimusPrime.logger import *
import numpy as np 
import pandas as pd
import argparse, sys
import os

def rastrygin(x, t1, t2):
	print('t1 = ', t1)
	print('t2 = ', t2)
	return 10*len(x) + np.sum(x*x - 10*np.cos(2*np.pi*x))
class RastriginDigitalTwin(AlgoDigitalTwin):
    def __init__(self):
        self.args = (1,2)

        # Use this when you wish to provide the initial position (x0)
        
        super().__init__(rastrygin)
        
        # Use this when you don't want to provide initial position (x0) - PSO ONLY-
        # super().__init__(rastrigin)

    def optimize(self, args, kwargs):
        if args.solver == 'basinhopping':
            kwargs['minimizer_kwargs']['args'] = self.args
        elif args.solver == 'GlobalBestPSO':
            kwargs['fun_kwargs'] = {
                't1': self.args[0],
                't2': self.args[1]
            }
        else:
            kwargs['args'] = self.args
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
		niter = 1
		tol = 1e-1
		niter_success = None
		stepsize = 0.5
		interval = 50
		kwargs = {
		'x0': utils.get_random_x0(20,-5.0,5.0),
		'niter':niter,
		'T': T,
		'stepsize':stepsize,
		'minimizer_kwargs': {
			'method':'powell',
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
		'x0': utils.get_random_x0((20,20),-5.0,5.0),
		'bounds':np.full((20,2), (-5.0, 5.0)),
		'strategy': 'best2exp',
		'maxiter':1,
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
		'workers': 1
		}

	elif args.solver == 'dual_annealing':
		def callback_(x,f,context):
			print("custom callback for dual_annealing")
			logger.info(fmt('info', "Dual Annealing Custom Callback Invoked"))
			return
		kwargs = {
		'x0': utils.get_random_x0(20,-5.0,5.0),
		'bounds':np.full((20,2), (-5.0, 5.0)),
		'tol': 1e-15,
		'initial_temp': 5230,
		'maxiter':1,
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
		'x0': utils.get_random_x0(20, -5.0,5.0),
		'method': 'nelder-mead',
		'tol': 1e-15,
		'callback':callback_,
		'maxiter':1,
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
		'maxiter':1,
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
		'maxiter':1,
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
			'maxfun':10,
			'maxls':10,
			'finite_diff_rel_step':None
		}

		}
	elif args.solver == 'GlobalBestPSO':
		kwargs = {
		'x0': utils.get_random_x0((400,20), -5.0,5.0),
		'dimensions':20,
		'bounds': np.full((20,2), (-5.0,5.0)),
		'maxiter':1,
		'n_particles':400,
		'options': {'c1':0.3,'c2': 0.65, 'w' : 0.95},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : None,
						'vh_strategy' : 'unmodified',
						'center' : 1.0,
						'ftol' : 1e-15
						}
		}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args, kwargs)
	else:
		cfg.main(RastriginDigitalTwin(), args, kwargs)


