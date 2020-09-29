
#  NOTE!  this is not being used!!!
#  Putting it here for reference....probably will revert back to it
#  at some point.
#
#
from ._basinhopping_solver import BasinhoppingSolver
from ._minimize_solver import MinimizeSolver
from OptimusPrime import  utils
import numpy as np

default_solver_params_dict = {

    'nelder-mead' : {
		'x0': utils.get_random_x0(5, -5.0,5.0),
		'method': 'nelder-mead',
		'tol': 1e-15,
		'maxiter':1000,
		'options': {
			'disp':0,
			'maxfev':None,
			'return_all':False,
			'xatol':0.1, # Currently doesn't work
			'fatol':0.1, # Currently doesn't work
			'adaptive':False
		}
		},
    
    # -------------------------------------
    'l-bfgs-b' : {
		'x0': utils.get_random_x0(5, -5.0,5.0),
		'method': 'l-bfgs-b',
		'jac':None,
		'bounds': np.full((5,2), (-5.0, 5.0)),
		'maxiter':1000,
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
		},
    
    # ------------------------------------

    'powell' : {
		'x0': utils.get_random_x0(5, -5.0,5.0),
		'method': 'powell',
		'tol': 1e-10,
		'bounds': np.full((5,2), (-5.0, 5.0)),
		'maxiter':1000,
		'options': {
			'disp':0,
			'maxfev':10000,
			'return_all':False,
			'xtol':1e-5, 
			'ftol':1e-5
		}
		},

    # -------------------------------------

    'cobyla' : {
		'x0': utils.get_random_x0(5,-5.0,5.0),
		'method': 'cobyla',
		'maxiter':1000000,
		'options': {
			'disp':0,
			'tol':1e-15,
			'catol':1e-15
		}
		},

    # --------------------------------------

    'basinhopping' : {
		'x0': utils.get_random_x0(5,-5.12,5.12),
		'niter':200,
		'T': 1.0,
		'stepsize': 0.5,
		'minimizer_kwargs': {
			'method':'powell',
            'options':{
            'maxiter':10, 
            } 
		},
		'tol':1e-12,
		'interval':50,
		'disp':0,
		'niter_success':None,
		'accept_test': None,
		'take_step': None
		},

    #-------------------------------------

    'differential_evolution' : {
		#  utils.get_random_x0(((popsize * #dv),#dv),min_value,max_value)
		'x0': utils.get_random_x0((5,5),-5.12,5.12),
		'bounds':np.full((5,2), (-5.12, 5.12)),
		'strategy': 'best2exp',
		'maxiter':80,
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
		},

    # ------------------------------------
    'dual_annealing' : {
		'x0': utils.get_random_x0(5,-5.12, 5.12),
		'bounds':np.full((5,2), (-5.12, 5.12)),
		'tol': 1e-15,
		'initial_temp': 5230,
		'maxiter':200,
		'restart_temp_ratio':2e-5,
		'visit':2.62,
		'accept':-2.0,
		'maxfun': 15000,
		'no_local_search': False,
		'seed': 20
		},

    # -------------------------------------

    'GlobalBestPSO' : {
		# 'x0': utils.get_random_x0((300,20), -5.12, 5.12),
		'x0': utils.get_static_x0((300,5), -5.12, 5.12, seed=3.0),
		'dimensions':5,
		'bounds': np.full((5,2), (-5.12,5.12)),
		'maxiter': 100,   #2750
		'n_particles':300,

		'options': {'c1':0.3,'c2': 0.65, 'w' : 0.95},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : None,
						'vh_strategy' : 'unmodified',
						'center' : 1.0,
						'ftol' : 1e-15,
						'ftol_iter' : 3
						}
		},
    
}