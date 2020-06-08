import argparse
import sys
import logging
import copy

default_solver_params_dict = {
	'nelder-mead' : {},
	'l-bfgs-b' : {},
	'powell' : {},
	'COBYLA' : {},
	'basinhopping' : {},
	'differential_evolution' : {},
	'dual_annealing' : {},
	'GlobalBestPSO' : {}
}


def get_default_params(solver_name):
	return copy.deepcopy(default_solver_params_dict.get(solver_name))

def get_commandline_args():
	print("Version:  ", sys.version)
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--solver", dest="solver", default='basinhopping', help="Solver to be used in optimization")
	parser.add_argument("-t", "--trace", action="store_true", help="enable code trading using pycallgraph")
	parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
	parser.add_argument("-z", "--silent-mode", action="store_true", help="Runs Optimus in silent mode ")
	args = parser.parse_args()

	if args.silent_mode:
		logger = logging.getLogger()
		logger.handlers = [ h for h in logger.handlers if not (type(h) == logging.StreamHandler)]
		print(logger.handlers)
		
	return args

def main(algo_wrapper, args, kwargs):
	print('Optimize using: ' + args.solver)
	print('x0: ', algo_wrapper.x0)
	print("args: ", args)
	print("kwargs", kwargs)


	#Origin:    res = algo_wrapper.optimize(args)

	res = algo_wrapper.optimize(args, kwargs)

	print("==================")
	print(res)
	# print('Global Minimum:  x = ', *res['x'])
	# print('f(x0) = ', res['fun'])

