from OptimusPrime import AlgoDigitalTwin, utils
from OptimusPrime.utils.functions.single_obj import rastrigin

import numpy as numpy

import argparse, sys

class RastriginDigitalTwin(AlgoDigitalTwin):

		def __init__ (self):
			dim = 20
			bnds = np.full((dim,2), (-5.12, 5.12))
			super().__init__(rastrigin, x=utils.get_random_x0(dim,-5.12, 5.12), bounds = bnds)

		def optimize(self, args):

			self.optimizer.update_solver_params('basinhopping', {'niter' : 1000} )

			return super().optimize(args)

if __name__ == '__main__':
	args = cfg.get_commandline_args()
	if args.trace:
		utils.run_with_callgraph(cfg.main, RastriginDigitalTwin(), args)
	else:
		cf.main(RastriginDigitalTwin(), args)


