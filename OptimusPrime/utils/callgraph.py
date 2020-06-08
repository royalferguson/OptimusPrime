from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput

def run_with_callgraph(main_func, algo_wrapper, args):

	config = Config()
	config.trace_filter = GlobbingFilter(exclude=['pyswarms.base.*',
										'pyswarms.utils.*',
										'numpy.*'],
										include=['OptimusDem.*',
										'RosenWithArgsDigitalTwin.*',
										'pyswarms.*optimize',
										'pyswarms.backend.*compute_objective_function',
										'main',
										'scipy.optimize.*basinhopping'])
	config.max_depth = 12
	graphviz = GraphvizOutput(output_file='optimus_rosen_trace.png', output_type='png')
	with PyCallGraph(output=graphviz, config=config):
		main_func(algo_wrapper, args)
