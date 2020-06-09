from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin
import OptimusPrime.configuration as cfg
import numpy as np 
import argparse, sys

class RastriginDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):
			dim = 20
			bnds = np.full((dim,2), (-5.12, 5.12))
			super().__init__(rastrigin, x0=utils.get_random_x0(dim,-5.12, 5.12), bounds = bnds)

		def optimize(self, args, **kwargs):
			return super().optimize(args, **kwargs)

if __name__ == '__main__':
	args = cfg.get_commandline_args()

	print("args:    ", args) 

	kwargs = {'niters':4}

	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args, **kwargs)
	else:
		cfg.main(RastriginDigitalTwin(), args, **kwargs)


