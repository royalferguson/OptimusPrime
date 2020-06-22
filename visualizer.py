from OptimusPrime.visualizer import Visualizer
import argparse
import sys
import logging
import copy
import os
from OptimusPrime.utils.display import set_global_frame,start_display_window

def is_path(string):
		#Verify valid file path
	if os.path.exists(string):
		return string
	else:
		raise NotADirectoryError(string)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required = True)
group.add_argument('-f', '--file', nargs=1, type=is_path, help='provide path to file for visulaizer to read them')
group.add_argument('-n', '--network', nargs='?', const='localhost', help='provide network for visualizer to recieve from optimus')
args = parser.parse_args()

v = Visualizer.getInstance()

if args.file:
	v.finish_init(file=args.file[0])
	v.read_file()
	set_global_frame(v.intermitent_data)
elif args.network:
    v.finish_init(host=args.network)
    v.start_receiving()
	

start_display_window()