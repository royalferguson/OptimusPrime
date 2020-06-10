from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin
import OptimusPrime.configuration as cfg
import numpy as np 
import argparse, sys

class RastriginDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):
			dim = 20
			bnds = np.full((dim,2), (-5.12, 5.12))
			# uncomment this when you want to provide x0
			super().__init__(rastrigin, x0 = utils.get_random_x0(10,-5.12, 5.12))
			# comment this when you want to provide x0
			# super().__init__(rastrigin)

		def optimize(self, args, **kwargs):
			return super().optimize(args, **kwargs)

if __name__ == '__main__':
	args = cfg.get_commandline_args()

	print("args:    ", args) 
	bnds = np.full((10,2), (-5.12, 5.12))
	
	"""
	#uncomment this when running with basinhopping
	def callback(xk,f, accept):
		print("custom callback")
	kwargs = {'niter':2,'callback':callback}
	""" 

	#try this then comment it
	#kwargs = {'dimension':10}
	# after you comment the above try this
	kwargs = {'bounds':bnds}
	# for basinhopping
	#kwargs = {'niter':2}
	# Full blown 
	"""kwargs = {
		'dimensions':10,
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
>>>>>>> 53e10215ec687eee630b59b8581ebcac686c1593

	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args, **kwargs)
	else:
		cfg.main(RastriginDigitalTwin(), args, **kwargs)


