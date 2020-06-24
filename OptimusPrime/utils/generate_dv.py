import os
import shutil
import sys
import argparse
import random
import numpy as np

def get_random_x0(count, lower=0, upper=1):
	variables=[]
	if isinstance(count, tuple):
		variables = np.random.uniform(lower, upper, (count[0], count[1]))
	else:
		for i in range (count):
			variables.append(random.uniform(lower,upper))
	variables = np.array(variables)
	return variables

if __name__=='__main__':
	parser = argparse.ArgumentParser(
		prog='ProgramName',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=text.dedent( '''\
			Example:
			example goes here...

			'''))
	parser.add_argument("-n", "--numDV", dest="numDV", type=int, default=100, help="Number of DVs to generate")
	parser.add_argument("-l", "--lower", dest="lb", type=int, default=0, help="Lower Bound (int)  Default = 0")
	parser.add_argument("-u", "--upper", dest="ub", type=int, default=1, help="Upper Bound (int)  Default = 1")
	parser.add_argument("-f", "--file", dest="outPutFile", default="DecisionVariables.csv", help="Output File Name")

	arrayDV.tofile(args.outPutFile, sep=",", format='%0.3f')
	print("Done")