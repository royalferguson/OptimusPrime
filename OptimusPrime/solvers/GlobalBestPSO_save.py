from pyswarms.single import GlobalBestPSO
from pyswarms.backend.operators import compute_pbest, compute_objective_function
import multiprocessing as multiprocessing
import logging


class _GlobalBestPSO(GlobalBestPSO):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs):
		fix_default_file_handler()

	def optimize(self, objective_func, iters, n_processes=None, verbose=False, silent=False, **kwargs):
		if verbose:
			logginglevel=logging.INFO
		if silent:
			remove_stream_handlers()
		self.rep.log("obj.func args: {}".format(kwargs), lvl=logging.DEBUG)
		self.rep.log("Optimize for {} iters with {}".format(iters, self.options), lvl=logginglevel)

		#populate memory of the handlers
		self.bh.memory = self.swarm.position
		self.vh.memory = self.swarm.position

		# Setup Pool of processes for parallel evaluation
		pool = None if n_processes is None else mp.Pool(n_processes)

		self.swarm.pbest_cost = np.full(self.swarm_size[0], np.inf)

		for i in range(iters) if not verbose or silent else self.rep.pbar(iters, self.name):
			# Compute cost for current position and personal best
			# fmt: off
			self.swarm.current_cost = compute_objective_function(self.swarm, objective_func, pool=pool, **kwargs)
			self.swarm.pbest_pos, self.swarm.pbest_cost = compute_pbest(self.swarm)
			# Set best_cost_yet_found for ftol
			best_cost_yet_found = self.swarm.best_cost
			self.swarm.best_pos, self.swarm.best_cost = self.top.compute_gbest(self.swarm)
			# fmt: on
			if verbose and not silent:
				self.rep.hook(best_cost=self.swarm.best_cost)
			# save to history
			hist = self.ToHistory(
				best_cost=self.swarm.best_cost,
				mean_pbest_cost=np.mean(self.swarm.pbest_cost),
				position=self.swarm.position,
				velocity=self.swarm.velocity,
				)
			self._populate_history(hist)
			# verify stop criteria based on the relative acceptable cost ftol
			relative_measure = self.ftol * (1 + np.abs(best_cost_yet_found))
			if (np.abs(self.swarm.best_cost - best_cost_yet_found) < relative_measure):
				break
			# perform velocity and position updates
			self.swarm.velocity = self.top.compute_velocity(self.swarm, self.velocity_clamp, self.vh, self.bounds)
			self.swarm.position = self.top.compute_position(self.swarm, self.bounds, self.bh)

		# obtain the final best_cost and the final best_position
		final_best_cost = self.swarm.best_cost.copy()
		final_best_pos = self.swarm.pbest_pos[self.swarm.pbest_cost.argmin()].copy()

		# write report in log and return final cost and position
		self.rep.log(
			"Optimization Finished | Best Cost: {}, Best Position: {}".format(final_best_cost, final_best_pos),
			lvl=logginglevel,
		)
		# close pool of processes
		if n_processes is not None:
			pool.close()
		return(final_best_cost, final_best_pos)




