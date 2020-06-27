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
    args.solver = 'dual_annealing'
    if os.path.exists('optimization_data.pkl'):
        os.remove('optimization_data.pkl')
    intermitentData = pd.DataFrame(columns=['solver','#DV', 'init_temp','restart_temp',
    'visit', 'accept', 'no_local_search','fun','niter','nfev'])
    # Initial_temp, original value is 5230
    init_temps = [10,1000,1500,2500,3500,4000,5000]
    # Restart temp ratio, default is 2e-5
    restart_temps = [1e-5,1e-3,1e-2,0.5,0.75]
    # Visit, default is 2.62
    visits = [1.5,2,2.36]
    # Accept, default is -5.0
    accepts = [-1e-5,-1,-2,-3]
    # no_local_search, default is true
    no_local_searches = [False]

    tols = [0.1,0.001,1e-9,1e-11,1e-12]
    def callback_(x,f,accept):
        print("custom callback for dual_annealing")
        logger.info(fmt('info', "dual_annealing Custom Callback Invoked"))
        return
    initial_temp = 5230
    restart_temp = 2e-5
    accept = -5.0
    visit = 2.62
    tol = 1e-5
    kwargs = {
        'x0': [-1.20555903e+00,  8.06886731e+00,  1.80761651e+00, -1.80190222e+00,
    9.14880298e+00, -4.66194875e+00, -1.99590416e+00,  1.71159707e+00,
    1.07142336e-01,  1.83666663e-01,  7.59412648e+00,  8.48575960e+00,
    -3.53197590e+00,  8.80976715e+00,  5.64708694e+00, -1.20210846e+00,
    -8.74750428e-01,  3.23924235e+00, -1.33689728e+00, -2.84890299e+00,
    6.32299907e+00,  5.33677456e+00,  6.65634924e+00,  3.76505176e+00,
    -2.30612880e+00,  4.59291716e+00, -4.57376326e+00, -3.42323031e+00,
    6.46603361e+00,  9.95147261e+00, -1.17810147e+00,  3.83084675e+00,
    -4.36706587e+00,  4.01634555e+00, -1.37749835e+00,  6.77345122e+00,
    3.44564212e-01,  8.41233930e+00,  1.71008261e+00, -4.81677489e+00,
    -2.36070242e+00, -2.96759374e+00,  2.93200910e+00,  7.91530059e-03,
    -4.29614946e-01,  9.00004519e+00, -1.66743106e-01,  7.07285525e+00,
    -3.33467345e+00,  2.24253078e+00],
        'bounds':np.full((50,2), (-5.0, 10.0)),
        'tol': tol,
        'initial_temp': initial_temp,
        'maxiter':10000,
        'restart_temp_ratio':restart_temp,
        'visit':visit,
        'accept':accept,
        'maxfun': 100000,
        'no_local_search': True,
        'seed': 20
        }
    app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
    intermitentData = intermitentData.append({'solver':'-------------------Default Parameters----------------',},ignore_index=True)
    intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
    )
    intermitentData = intermitentData.append({'solver':'-------------------Initial_temp Trials----------------',},ignore_index=True)
    for i in init_temps:
        kwargs.update({'initial_temp':i})
        app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
        intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
        )
    kwargs.update({'initial_temp':initial_temp})
    intermitentData = intermitentData.append({'solver':'------------------- Restart_temp_ratio Trials----------------',},ignore_index=True)
    for i in restart_temps:
        kwargs.update({'restart_temp_ratio':i})
        app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
        intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
        )
    kwargs.update({'restart_temp_ratio':restart_temp})
    intermitentData = intermitentData.append({'solver':'------------------- Visit Trials----------------',},ignore_index=True)
    for i in visits:
        kwargs.update({'visit':i})
        app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
        intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
        )
    kwargs.update({'visit':visit})
    intermitentData = intermitentData.append({'solver':'------------------- Accept Trials----------------',},ignore_index=True)
    for i in accepts:
        kwargs.update({'accept':i})
        app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
        intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
        )
    kwargs.update({'accept':accept})

    intermitentData = intermitentData.append({'solver':'------------------- Tolerance Trials----------------',},ignore_index=True)
    for i in tols:
        kwargs.update({'tol':i})
        app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
        intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
        )
    kwargs.update({'tol':tol})
    intermitentData = intermitentData.append({'solver':'-------------------  No Local Search Trials----------------',},ignore_index=True)

    for i in no_local_searches:
        kwargs.update({'no_local_search':i})
        app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
        intermitentData = intermitentData.append({
            'solver':'dual_annealing',
            '#DV':50,
            'initial_temp':kwargs['initial_temp'],
            'accept':kwargs['accept'],
            'visit':kwargs['visit'],
            'restart_temp_ratio':kwargs['restart_temp_ratio'],
            'no_local_search':kwargs['no_local_search'],
            'fun': app.fun,
            'niter':app.nit,
            'nfev': app.nfev
        },ignore_index=True
        )
    kwargs.update({'no_local_search':True})

    intermitentData.to_csv('data.csv')
