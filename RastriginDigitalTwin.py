from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin
import OptimusPrime.configuration as cfg
import numpy as np 
import argparse, sys

class RastriginDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):
			super().__init__(rastrigin)

		def Initialize_Starting_Position(self,x0):
			self.x0 = x0

		def optimize(self, args, **kwargs):
			return super().optimize(args, **kwargs)

if __name__ == '__main__':
	args = cfg.get_commandline_args()

	print("args:    ", args) 


	bnds = np.full((10,2), (-5.12, 5.12))
	def callback_(x,f,accept):
		print("custom callback for basinhopping")
		return
	# for basinhopping
	x0 = utils.get_random_x0(10,-5.12, 5.12)

	kwargs = {'niter':2,
	'T': 0.2,
	'stepsize':0.65,
	'minimizer_kwargs': {
		'method':'BFGS'
	},
	'interval':2,
	'disp':1,
	'niter_success':2,
	'accept_test': None,
	'take_step': None,
	'callback': callback_,
	'seed': 20
	}
	# for pso
	"""kwargs = {
		'dimension':10,
		'bounds':bnds,
		'maxiter':100,
		'n_particles':200,
		'options': {'c1':0.5,'c2': 0.7, 'w' : 0.85},
		'pso_kwargs': {'bh_strategy' : 'periodic',
						'velocity_clamp' : (1,2),
						'vh_strategy' : 'unmodified',
						'center' : 2,
						'ftol' : -1
						}
	}"""

	class_ = RastriginDigitalTwin()
	#comment/uncomment next line when you want to add a starting position
	class_.Initialize_Starting_Position(x0)

	if args.trace:
		utils.run_with_callgraph(cfg.main, class_, args, **kwargs)
	else:
		cfg.main(class_, args, **kwargs)


