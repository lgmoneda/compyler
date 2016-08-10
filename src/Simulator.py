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
		super(Simulator, self).__init__()
		self.granularity = "line"
		self.inputFile = "../data/input1.txt"
		self.input = []
		self.outer_engine = OuterEngine("Outer Engine")
		self.verboseOptions = {"Listing": verbose,
						 	   "Block Track": verbose}
		
	def showOptionsWait(self):
		"""Shows a menu option

		Display all the options the user has in the simulation. Get what is typed,
		and pass it to be treated.

		Returns:
			A boolean that if is True indicates the end of the simulation. 

		"""
		print "\nChoose your destiny: "
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
		print "(e) Change granularity",
		print "(f) Finish"

		user_input = raw_input()
		return self.treatUserInput(user_input)
	
	def treatUserInput(self, userInput):
		if userInput == "a":
			self.askForInput()
		if userInput == "b":
			self.simulate()
		if userInput == "c":
			self.switchVerboseOption("Listing")
		if userInput == "d":
			self.switchVerboseOption("Block Track")
		if userInput == "e":
			self.granularityChange()
		if userInput == "f":
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
		self.verboseOptions[key] = not self.verboseOptions[key]
		self.printVerboseOptions()

	def printVerboseOptions(self):
		print "\nTrack Options: "
		for key, value in self.verboseOptions.iteritems():
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
		self.inputFile = raw_input("\nInform the input file name: ")

	def granularityChange(self):
		"""Asks for granularity definition
		"""
		print "\nWorking granularity: " + self.granularity
		print "Define as: "
		answer = raw_input("(a) Line (b) Word (c) Character: ")

		options = {"a": "line", "b": "word", "c": "char"}
		self.granularity = options.get(answer, "line") 


	def createInitialInput(self):
		self.input = []
		with open(self.inputFile) as f:
			for line in f:
				if self.granularity == "line":
					#Taking out the \n from line
					line = line.replace("\n", "")
					self.input.append(line)
				if self.granularity == "word":
					for word in line.split():
						self.input.append(word)
				if self.granularity == "char":
					for word in line.split():
						for char in word:
							self.input.append(char)

	def simulate(self):
		self.createInitialInput()
		self.outer_engine.setup(self.input, self.granularity, self.verboseOptions)
		return self.outer_engine.run()