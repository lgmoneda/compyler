from OuterEngine import OuterEngine


class Simulator(object):
	"""The simulation and user interaction manager, the Simulator!

	This class should handle user options over the simulation, let them choosing
	between many track options, to define input file, run the simulation and
	terminate it.

	It won't be event based, it just starts the outer engine that will.

	Args:
		verbose: A boolean indicating the initial state of all verbose options

	Attributes:
		verboseOptions: A dict with many tracking options as keys and a boolean
			value indicating if we'll print it 
	"""
	def __init__(self, verbose=True):
		super(Simulador, self).__init__()
		self.fileInput = None
		self.verboseOptions = {"Listing": verbose,
						 	   "Block Track": verbose}
		
	def showOptionsWait(self):
		"""Shows a menu option

		Display all the options the user has in the simulation. Get what is typed,
		and pass it to be treated.

		Returns:
			A boolean that if is True indicates the end of the simulation. 

		"""
		print "Choose your destiny: "
		print "(a) Choose Input",
		print "(b) Run Simulation",
		if self.verboseOptions["Listing"]: 
			print "(c) Turn off input listing", 
		else: 
			print "(c) Turn on input listing", 
		if self.verboseOptions["Block Track"]: 
			print "(d) Turn off block track", 
		else: 
			print "(d) Turn on block track", 
		print "(e) Finish"


		user_input = raw_input()
		return self.treatUserInput(user_input)
	
	def treatUserInput(self, userInput):
		if event == "a":
			self.askForInput()
		if event == "b":
			self.simulate()
		if event == "c":
			pass
		if event == "d":
			pass
		if event == "e":
			return self.finishSimulation()

		return False

	def getVerboseOptions(self):
		return self.verboseOptions

	def switchVerboseOption(self, key):
		"""Switch a single verbose option 

		Args:
			key: a string representing the verbose option name to be switched
		Returns:
			updated verboseOptions
		"""
		self.verboseOptions[key] = not value

	def printVerboseOptions(self):
		print "Track Options: "
		for key, value in verboseOptions.iteritems():
			print key + ": ",
			if value:
				print "On"
			else:
				print "Off"

	def finishSimulation(self):
		"""
		"""
		return True

	def run(self):
		"""Simulator loop

		Keeps looping until the user chooses the 'finish' option.  
		"""
		end = False
		while not end:
			end = self.showOptionsWait()

	def askForFileName(self):
		"""Ask user for the input file name
		"""
		self.fileInput = raw_input("Inform the input file name: ")


	def simulate(self):
		return outerEngine.run(self.fileInput)