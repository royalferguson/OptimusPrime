import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk 
from tkinter import ttk 
import matplotlib.ticker as ticker 

dfObj = pd.DataFrame()  #global variable, dataframe that is take from the visualizer to be used for the display
def set_global_frame(df):
	#  Function retrieves data frame that the visualizer reads from the pickle file
	#  Called in the visualizer, then stores it in the global dataframe 

	global dfObj
	dfObj = df

class VisualizerDisplay(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "Visualizer Client")

		container = tk.Frame(self)
		container.pack(side='top', fill="both", exapand = True)
		container.grid_rowconfigure(0, weight=1)
		self.frames = {}

		for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix, PageSeven, PageEight, PageNine):
			frame = F(container, self)
			self.frames[F] = frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
	# Home page of the visual display - allows navigation to any other page
		tk.Frame.__init_self(self, parent)
		label = tk.Label(self, tex="Home Page")
		label.pack(pady=10, padx=10)
		# Button setup for the home page

		button = ttk.Button(self, text="Score vs Iteration", width=30, command=lambda:controller.show_frame(PageOne))

		button.pack()
		button = ttk.Button(self, text="Scores(log) vs Iteration", width=30, command=lambda:controller.show_frame(PageTwo))
		button.pack()
		button = ttk.Button(self, text="DV Values", width=30, command=lambda:controller.show_frame(PageThree))
		button.pack()
		button = ttk.Button(self, text="DV-Ave Values", width=30, command=lambda:controller.show_frame(PageFour))
		button.pack()
		button = ttk.Button(self, text="DV-RMS Values", width=30, command=lambda:controller.show_frame(PageFive))
		button.pack()
		button = ttk.Button(self, text="DV Values - Heat Map", width=30, command=lambda:controller.show_frame(PageSix))
		button.pack()
		button = ttk.Button(self, text="DV-AVE Values - Heat Map", width=30, command=lambda:controller.show_frame(PageSeven))
		button.pack()
		button = ttk.Button(self, text="sqrt (DV-RMS) Values - Heat Map", width=30, command=lambda:controller.show_frame(PageEight))
		button.pack()
		button = ttk.Button(self, text="DV-RMS Values -Heat Map", width=30, command=lambda:controller.show_frame(PageNine))
		button.pack()

class PageOne(tk.Frame):
	'''  Initializes the first page of the gui..graph embedded into it, also adds columns to the data frame
		 for use in later graphs...
		 All, pages or tabs have their own class and are set up the same way...but with different graphs embedded in them
	'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self)
		label.pack(pady=0, padx=0)

		''' Button initializers, for the display navigation, can go to any other tab or back to the home page
		all buttons are inside frames on the page for organization, all classes are set up the same way'''
		top = tk.Frame(self)
		middle = tk.Frame(self)
		top.pack(side='top')
		middle.pack(side='top')
		bottom = tk.Frame(self)
		bottom.pack(side='top')

		next = ttk.Button(self, text="Next >>", width = 25, command=lambda: controller.show_frame(PageTwo))
		next.pack(in_=top, side='left')
		one = ttk.Button(self, text="Score(log)", width=25, command=lambda:  controller.show_frame(PageTwo))
		one.pack(in_=middle, side='left')
		two = ttk.Button(self, text="DV Values", width=25, command=lambda:  controller.show_frame(PageThree))
		two.pack(in_=middle, side='left')
		three = ttk.Button(self, text="DV-AVE Values", width=25, command=lambda:  controller.show_frame(PageFour))
		three.pack(in_=middle, side='left')
		four = ttk.Button(self, text="DV-RMS Values", width=25, command=lambda:  controller.show_frame(PageFive))
		four.pack(in_=middle, side='left')
		five = ttk.Button(self, text="DV Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageSix))
		five.pack(in_=middle, side='left')
		six = ttk.Button(self, text="DV-AVE Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageSeven))
		six.pack(in_=middle, side='left')
		seven = ttk.Button(self, text="sqrt(DV-RMS) Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageEight))
		seven.pack(in_=middle, side='left')
		eight = ttk.Button(self, text="DV-RMS Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageNine))
		eight.pack(in_=middle, side='left')
		previous = ttk.Button(self, text="<< Previous", width=25, command=lambda:  controller.show_frame(PageNine))
		previous.pack(in_=bottom, side='left')
		home = ttk.Button(self, text="Home Page", width=25, command=lambda:  controller.show_frame(StartPage))
		home.pack(in_=bottom, side='left')

		dfObj['score'] = 1e-6 + dfObj['score']
		dfObj['length'] = dfObj['dv'].str.len()
		OF_min = dfObj['score'].min()
		OF_max = dfObj['score'].max()
		n_evals=len(dfObj)
		nsmooth = int(max([0.01*n_evals, 10]))

		for ix in range(dfObj['length'][0]):
			xvals = dfObj['dv'].str[ix].Values
			xave = np.zeros(len(xvals))
			xrms = np.zeros(len(xvals))
			for ipt in range(nsmooth,len(xvals)):
				use_points = xvals[ipt-nsmooth:ipt]
				xave[ipt] = use_points.mean()
				xrms[ipt] = use_points.std()
			for ipt in range(nsmooth):
				xave[ipt] = 0.0
				xrms[ipt] = 0.0
			dfObj['dv' + str(ix)+'ave'] = xave
			dfObj['dv'+str(ix)+"rms"] = xrms
		# Graph for score vs iteration
		fig, ax = plt.subplots(figsize=(15,4))
		ax.set_title("Score Values vs Iteration")
		ax.set_xlabel("Iteration Number")
		ax.set_ylabel("Score")
		dfObj['score'].plot(figsize=(8,6), ylim=(0, OF_max*1.02), rasterized=True)

		canvas=FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		plt.close()

class PageTwo(tk.Frame):
	'''  Initializes the first page of the gui..graph embedded into it, also adds columns to the data frame
		 for use in later graphs...
		 All, pages or tabs have their own class and are set up the same way...but with different graphs embedded in them
	'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self)
		label.pack(pady=0, padx=0)

		''' Button initializers, for the display navigation, can go to any other tab or back to the home page
		all buttons are inside frames on the page for organization, all classes are set up the same way'''
		top = tk.Frame(self)
		middle = tk.Frame(self)
		top.pack(side='top')
		middle.pack(side='top')
		bottom = tk.Frame(self)
		bottom.pack(side='top')

		next = ttk.Button(self, text="Next >>", width = 25, command=lambda: controller.show_frame(PageThree))
		next.pack(in_=top, side='left')
		one = ttk.Button(self, text="Score vs Iteration", width=25, command=lambda:  controller.show_frame(PageOne))
		one.pack(in_=middle, side='left')
		two = ttk.Button(self, text="DV Values", width=25, command=lambda:  controller.show_frame(PageThree))
		two.pack(in_=middle, side='left')
		three = ttk.Button(self, text="DV-AVE Values", width=25, command=lambda:  controller.show_frame(PageFour))
		three.pack(in_=middle, side='left')
		home = ttk.Button(self, text="DV-RMS Values", width=25, command=lambda:  controller.show_frame(StartFive))
		home.pack(in_=bottom, side='left')
		four = ttk.Button(self, text="DV Values - Heat", width=25, command=lambda:  controller.show_frame(PageSix))
		four.pack(in_=middle, side='left')
		five = ttk.Button(self, text="DV -AVE Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageSeven))
		five.pack(in_=middle, side='left')
		six = ttk.Button(self, text="sqrt(DV-RMS) Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageEight))
		six.pack(in_=middle, side='left')
		seven = ttk.Button(self, text="DV-RMS Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageNine))
		seven.pack(in_=middle, side='left')
		previous = ttk.Button(self, text="<< Previous", width=25, command=lambda:  controller.show_frame(PageOne))
		previous.pack(in_=bottom, side='left')
		home = ttk.Button(self, text="Home Page", width=25, command=lambda:  controller.show_frame(StartPage))
		home.pack(in_=bottom, side='left')


		# Graph for score vs iteration
		fig, ax = plt.subplots(figsize=(15,4))
		ax.set_title("Log(ScoreValues) vs Iteration")
		ax.set_xlabel("Iteration Number")
		ax.set_ylabel("Score")
		OF_max = dfObj["score"].max()
		dfObj['score'].plot(figsize=(8,6), ylim=(0, OF_max*1.02), rasterized=True)

		canvas=FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		plt.close()


	'''  Initializes the first page of the gui..graph embedded into it, also adds columns to the data frame
		 for use in later graphs...
		 All, pages or tabs have their own class and are set up the same way...but with different graphs embedded in them
	'''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self)
		label.pack(pady=0, padx=0)

		''' Button initializers, for the display navigation, can go to any other tab or back to the home page
		all buttons are inside frames on the page for organization, all classes are set up the same way'''
		top = tk.Frame(self)
		middle = tk.Frame(self)
		top.pack(side='top')
		middle.pack(side='top')
		bottom = tk.Frame(self)
		bottom.pack(side='top')

		next = ttk.Button(self, text="Next >>", width = 25, command=lambda: controller.show_frame(PageThree))
		next.pack(in_=top, side='left')
		one = ttk.Button(self, text="Score vs Iteration", width=25, command=lambda:  controller.show_frame(PageOne))
		one.pack(in_=middle, side='left')
		two = ttk.Button(self, text="DV Values", width=25, command=lambda:  controller.show_frame(PageThree))
		two.pack(in_=middle, side='left')
		three = ttk.Button(self, text="DV-AVE Values", width=25, command=lambda:  controller.show_frame(PageFour))
		three.pack(in_=middle, side='left')
		home = ttk.Button(self, text="DV-RMS Values", width=25, command=lambda:  controller.show_frame(StartFive))
		home.pack(in_=bottom, side='left')
		four = ttk.Button(self, text="DV Values - Heat", width=25, command=lambda:  controller.show_frame(PageSix))
		four.pack(in_=middle, side='left')
		five = ttk.Button(self, text="DV -AVE Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageSeven))
		five.pack(in_=middle, side='left')
		six = ttk.Button(self, text="sqrt(DV-RMS) Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageEight))
		six.pack(in_=middle, side='left')
		seven = ttk.Button(self, text="DV-RMS Values - Heat Map", width=25, command=lambda:  controller.show_frame(PageNine))
		seven.pack(in_=middle, side='left')
		previous = ttk.Button(self, text="<< Previous", width=25, command=lambda:  controller.show_frame(PageOne))
		previous.pack(in_=bottom, side='left')
		home = ttk.Button(self, text="Home Page", width=25, command=lambda:  controller.show_frame(StartPage))
		home.pack(in_=bottom, side='left')


		# Graph for score vs iteration
		fig, ax = plt.subplots(figsize=(15,4))
		ax.set_title("Log(ScoreValues) vs Iteration")
		ax.set_xlabel("Iteration Number")
		ax.set_ylabel("Score")
		OF_max = dfObj["score"].max()
		dfObj['score'].plot(figsize=(8,6), ylim=(0, OF_max*1.02), rasterized=True)

		canvas=FigureCanvasTkAgg(fig, self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		plt.close()

# And so on for 9 page classes

def start_display_window():
	# Functions that starts the Visualizaton, function gets called inside the Visualizer
	app = VisualizerDisplay()
	app.mainloop()

	
