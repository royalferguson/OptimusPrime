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
	intermitentData = pd.DataFrame(columns=['solver','#DV','T', 'stepsize','interval','niter_limit', 'niter_success', 'tol','fun','niter','nfev'])
	Ts = [0.1,0.5,1.5]
	stepsizes = [0.1,0.2,0.25,0.35,0.4,0.45]
	intervals = [5,40,75]
	niter_successes = [1,5,10]
	tols = [0.1,0.01,1e-09,1e-11,1e-12]
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
	intermitentData = intermitentData.append({'solver':'-------------------Default Parameters----------------',},ignore_index=True)
	intermitentData = intermitentData.append({
		'T':kwargs['T'],
		'interval':kwargs['interval'],
		'niter_success':kwargs['niter_success'],
		'tol':kwargs['tol'],
		'stepsize':kwargs['stepsize'],
		'niter_limit':kwargs['niter'],
		'fun': app.fun,
		'niter':app.nit,
		'nfev': app.nfev
	},ignore_index=True
	)
	intermitentData = intermitentData.append({'solver':'-------------------T Trials----------------',},ignore_index=True)
	for i in Ts:
		kwargs.update({'T':i})
		app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
		intermitentData = intermitentData.append({
			'solver':'basinhopping',
			'#DV':50,
			'T':kwargs['T'],
			'interval':kwargs['interval'],
			'niter_success':kwargs['niter_success'],
			'tol':kwargs['tol'],
			'stepsize':kwargs['stepsize'],
			'niter_limit':kwargs['niter'],
			'fun': app.fun,
			'niter':app.nit,
			'nfev': app.nfev
		},ignore_index=True
		)
	kwargs.update({'T':T})
	intermitentData = intermitentData.append({'solver':'------------------- Interval Trials----------------',},ignore_index=True)
	for i in intervals:
		kwargs.update({'interval':i})
		app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
		intermitentData = intermitentData.append({
			'solver':'basinhopping',
			'#DV':50,
			'T':kwargs['T'],
			'interval':kwargs['interval'],
			'niter_success':kwargs['niter_success'],
			'tol':kwargs['tol'],
			'stepsize':kwargs['stepsize'],
			'niter_limit':kwargs['niter'],
			'fun': app.fun,
			'niter':app.nit,
			'nfev': app.nfev
		},ignore_index=True
		)
	kwargs.update({'interval':interval})
	intermitentData = intermitentData.append({'solver':'-------------------stepsize Trials----------------',},ignore_index=True)
	for i in stepsizes:
		kwargs.update({'stepsize':i})
		app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
		intermitentData = intermitentData.append({
			'solver':'basinhopping',
			'#DV':50,
			'T':kwargs['T'],
			'interval':kwargs['interval'],
			'niter_success':kwargs['niter_success'],
			'tol':kwargs['tol'],
			'stepsize':kwargs['stepsize'],
			'niter_limit':kwargs['niter'],
			'fun': app.fun,
			'niter':app.nit,
			'nfev': app.nfev
		},ignore_index=True
		)
	kwargs.update({'stepsize':stepsize})
	intermitentData = intermitentData.append({'solver':'-------------------niter_success Trials----------------',},ignore_index=True)
	for i in niter_successes:
		kwargs.update({'niter_success':i})
		kwargs.update({'tol':1e-15})
		app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
		intermitentData = intermitentData.append({
			'solver':'basinhopping',
			'#DV':50,
			'T':kwargs['T'],
			'interval':kwargs['interval'],
			'niter_success':kwargs['niter_success'],
			'tol':kwargs['tol'],
			'stepsize':kwargs['stepsize'],
			'niter_limit':kwargs['niter'],
			'fun': app.fun,
			'niter':app.nit,
			'nfev': app.nfev
		},ignore_index=True
		)
	kwargs.update({'niter_success':niter_success})
	kwargs.update({'tol':1e-5})
	
	intermitentData = intermitentData.append({'solver':'------------------- Tolerance Trials----------------',},ignore_index=True)
	for i in tols:
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
	'niter':niter,
	'T': T,
	'stepsize':stepsize,
	'minimizer_kwargs': {
		'method':'BFGS'
	},
	'interval':interval,
	'disp':0,
	'tol': i,
	'niter_success':niter_success,
	'accept_test': None,
	'take_step': None,
	'seed': 20
	}
		app = (cfg.main(RosenbrockDigitalTwin(), args, kwargs))
		intermitentData = intermitentData.append({
			'solver':'basinhopping',
			'#DV':50,
			'T':kwargs['T'],
			'interval':kwargs['interval'],
			'niter_success':kwargs['niter_success'],
			'tol':kwargs['tol'],
			'stepsize':kwargs['stepsize'],
			'niter_limit':kwargs['niter'],
			'fun': app.fun,
			'niter':app.nit,
			'nfev': app.nfev
		},ignore_index=True
		)
	intermitentData.to_csv('data.csv')

