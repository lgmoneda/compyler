from OuterEngine import OuterEngine
from FrontEngine import FrontEngine
from LexicalAnalysis import LexicalAnalysis
from SyntacticEngine import SyntacticEngine
from SemanticEngine import SemanticEngine
from BackEngine import BackEngine
import re

class Simulator(object):
	"""The simulation and user interaction manager, the Simulator!

	This class should handle user options over the simulation, let them choosing
	between many track options, to define input file, run the simulation and
	terminate it.

	It won't be event based, it just holds the engines that will. It can be considered
	the outer box in the schema given, the big compiler box. Contains all the small
	boxes (engines) that process the input in each stage.

	Args:
		verbose: A boolean indicating the initial state of all verbose options

	Attributes:
		granularity: specifies the treatable unit, it can be line, word or character.
		verboseOptions: A dict with many tracking options as keys and a boolean
			value indicating if we'll print it .
		inputFile: the input file name and location.
		input: the input after reading it from file.
		engines: the list of engines the compiler contains inside. 
	"""
	def __init__(self, verbose=True):
		super(Simulator, self).__init__()
		self.granularity = "char"
		self.inputFile = "../data/grammarMin.txt"
		#self.inputFile = "../data/prog1.txt"
		self.input = []
		self.engines = []
		self.engines.append(OuterEngine("Outer Engine"))
		self.engines.append(LexicalAnalysis("Lexical Analysis"))
		self.engines.append(SyntacticEngine("Syntactic Analysis"))
		#self.engines.append(FrontEngine("FrontEnd"))
		self.engines.append(SemanticEngine("Semantic"))
		self.engines.append(BackEngine("BackEnd"))

		self.verboseOptions = {"Listing": verbose,
						 	   "Block Track": verbose,
						 	   "Event Track": True}
		
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
		print "(f) Step Process",
		if self.verboseOptions["Event Track"]: 
			print "(g) Turn off event track", 
		else: 
			print "(g) Turn on event track", 
		print "(z) Finish"
		

		user_input = raw_input()
		return self.treatUserInput(user_input)
	
	def treatUserInput(self, userInput):
		"""decide which action respond user input

		Call a method to treat the user input. 

		Args:
			userInput: the character the user typed and raw_input has captured.
		"""
		if userInput == "a":
			self.askForFileName()
		if userInput == "b":
			self.simulate()
		if userInput == "c":
			self.switchVerboseOption("Listing")
		if userInput == "d":
			self.switchVerboseOption("Block Track")
		if userInput == "e":
			self.granularityChange()
		if userInput == "z":
			return self.finishSimulation()
		if userInput == "f":
			self.stepSimulate()
		if userInput == "g":
			self.switchVerboseOption("Event Track")

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
		"""Display verbose options for simulation
		"""
		print "\nTrack Options: "
		for key, value in self.verboseOptions.iteritems():
			print key + ": ",
			if value:
				print "On"
			else:
				print "Off"

	def finishSimulation(self):
		"""Terminates simulation
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
		self.inputFile = "../data/" + raw_input("\nInform the input file name: ")

	def granularityChange(self):
		"""Asks for granularity definition
		"""
		print "\nWorking granularity: " + self.granularity
		print "Define as: "
		answer = raw_input("(a) Line (b) Word (c) Character: ")

		options = {"a": "line", "b": "word", "c": "char"}
		self.granularity = options.get(answer, "line") 


	def createInitialInput(self):
		"""Opens input file and turn it into input

		Depending on the granularity, constructs the input reading the input 
		file indicated by the user.
		"""
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
					for word in re.split(r'(\s+)', line):
					#for word in line.split(""):
						for char in word:
							self.input.append(char)

	def simulate(self):
		"""Starts the simulation

		Create the initial input from the file and feeds the first engine.
		Then, make all of them run and feed each other, being the input from
		a given engine the output from the previous one.

		Returns:
			A boolean indicating or not the success of the simulation.
		"""
		self.createInitialInput()
		input_ = self.input
		for engine in self.engines:
			engine.setup(input_, self.granularity, self.verboseOptions)

			if not engine.run():
				return False
			input_ = engine.getOutput()
			#print "inputs -> outputs"
			#print input_

		for item in input_:
			#print item
			print ""
			print item["value"],
			print item["category"],

		print "Successful simulation."
		return True

	def stepSimulate(self):
		"""Process the input file one unit each time
		"""
		self.createInitialInput()
		while len(self.input) != 0:
			input_ = self.input[0]
			self.input = self.input[1:]
			for engine in self.engines:
				engine.setup(input_, self.granularity, self.verboseOptions)
				if not engine.run():
					return False
				input_ = engine.getOutput()
			raw_input("Press any button to process the next unit...")

		print "\nSuccessful simulation."
		return True
