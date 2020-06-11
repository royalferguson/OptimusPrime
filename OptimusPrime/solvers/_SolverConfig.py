
#  NOTE!  this is not being used!!!
#  Putting it here for reference....probably will revert back to it
#  at some point.
#
#
from ._basinhopping_solver import BasinhoppingSolver
from ._minimize_solver import MinimizeSolver
solver_dict = {
    #'Nelder-Mead' : MinimizeSolver('Nelder-Mead'),
    'l-bfgs-b' : MinimizeSolver('l-bfgs-b'),
    # 'GlobalBestPSO' : ParticleSwarmSolver(),
    'differential_evolution' : DifferentialEvolutionSolver(),
    'basinhopping' : BasinhoppingSolver()
}


default_solver_params_dict = {

    'nelder-mead' : {
    'class' : 'PySciMin',
    'tol': 1e-6,
    'callback' : None,
    'options' : {
        'xatol': 1e-8,
        'fatol' : 1e-8,
        'maxiter': int(10e2),
        'maxfev': int(10e5),
        'initial_simplex': None,
        'adaptive': True,
        'disp': False
        }
    },
    
    # -------------------------------------
    'l-bfgs-b' : {
    'class' : 'PySciMin',
    'jac' : None,
    'bounds' : None,
    'tol' : 1e-6,
    'options' : {
        'maxcor': None,
        'maxiter': int(10e2),
        'maxfun': int(10e2),
        'ftol': 10e-18,
        'gtol': 10e-18,
        'eps' : None,
        'iprint' : None,
        'callback' : None,
        'maxls' : None,
        'disp': False
        },
    'callback' : None
    },
    
    # ------------------------------------

    'powell' : {
    'class' : 'PySciMin',
    'tol' : 1e-6,
    'options' : {
        'disp' : False,
        'xtol' : None,
        'ftol' : None,
        'maxiter': int(10e2),
        'maxfev': int(10e2),
        'direc' : None
        },
    'callback' : None
    },

    # -------------------------------------

    'COBYLA' : {
    'class' : 'PySciMin',
    'constraints' : [],
    'tol' : 1e-6,
    'options' : { 
        'rhobeg' : None,
        'tol' : 1e-6,
        'disp' : False,
        'maxiter': int(10e2),
        'catol' : None
        },
    'callback' : None
    },

    # --------------------------------------

    'basinhopping' : {
    'class' : 'PySciMethod',
    'niter' : int(10),
    'T' : 1.0,
    'stepsize' : 0.5,
    'minimizer_kwargs': {'method' : 'L-BFGS-B' },
    'take_step' : None,
    'accept_test': None,
    'callback' : "logging.log_scipy_basinhopping",
    'interval' : 50,
    'disp': 0,
    'niter_success' : None,
    'seed' : None,
    'callback' : None
    },

    #-------------------------------------

    'differential_evolution' : {
    'class' : 'PySciMethod',
    'bounds' : None,
    'strategy' : 'best1bin',
    'maxiter' : int(10e2),
    'popsize' : None,
    'tol' : None,
    'atol' : None,
    'mutation' : None,
    'recombination' : None,
    'seed' : None,
    'disp': False,
    'polish' : None,
    'init' : 'latinhypercube',
    'atol' : None,
    'updating' : None,
    'workers' : None,
    'constraints' : None,
    'callback' : None
    
    },

    # ------------------------------------
    'dual_annealing' : {
    'class' : 'PySciMethod',
    'bounds' : None,
    'maxiter': int(10e2),
    'local_search_options':{},
    'initial_temp':5230.0,
    'restart_temp_ratio':2e-05,
    'visit':2.62, 
    'accept':- 5.0, 
    'maxfun':1e4, 
    'seed': None, 
    'no_local_search':False, 
    'callback' : None
    },

    # -------------------------------------

    'pso_global_optimize' : {
    'class' : 'PartSwarm',
    'iters' : 4000,
    'n_particles' : 100,
    'n_processes' : None,
    'init_pos' : None,
    'bounds' : None,
    'options' : { 
        'c1': 0.2,
        'c2': 0.6,
        'w': 0.95 },
    'ftol' : 1e-6,
    'ftol_iter': 10,
    'bh_strategy' : 'Random',
    'vh_strategy' : 'unmodified',
    'center' :  1.0,
    'velocity_clamp' : None
    }
    
}