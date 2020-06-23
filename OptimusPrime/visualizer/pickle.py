import pandas as pd 
import pickle
from OptimusPrime.utils.decorators import add_method

@add_method(pd.series)
def add_to_pickle(item, path):
	with open(path, 'ab') as file:
		pickle.dump(item, file)

def read_from_pickle(path):
	with open(path, 'rb') as file:
		try:
			while True:
				yield pickle.load(file)
		except EOFError:
			pass