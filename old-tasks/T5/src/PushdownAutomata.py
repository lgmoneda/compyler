from Engine import Engine
from FiniteAutomata import FiniteAutomata

class PushdownAutomata(Engine):

	def __init__(self, name, def_file, key):
		super(PushdownAutomata, self).__init__(name)
		self.key = key
		self.submachines = []
		self.submachines_names = []
		self.n_submachines = None

		self.ProcessDescriptions(def_file)

	def ProcessDescriptions(self, def_file):
		with open(def_file) as f:
			self.n_submachines = int(f.next())
			for i in range(self.n_submachines):
				name = f.next()[:-1]
				self.submachines_names.append(name)
				line = f.next()
				text_file = open("AF_temporario.txt", "w")
				while line != "@\n":
					text_file.write(line)
					line = f.next()
				text_file.close()
				self.submachines.append(FiniteAutomata(name, def_file="AF_temporario.txt", key=self.key))		
		for submachine in self.submachines:
			submachine.setSubmachines(self.submachines)
			submachine.setup(self.inputs, self.granularity, self.verboseOptions)

	def event1Handler(self, event):
		for submachine in self.submachines:
			submachine.setSubmachines(self.submachines)
			submachine.setup(self.inputs, self.granularity, self.verboseOptions)

		mainmachine_input = []
		for event_ in self.eventsList:
			mainmachine_input.append(event_["content"])
		self.submachines[0].setup(mainmachine_input, self.granularity, self.verboseOptions)
		#####self.submachines[0].setEventsList(self.eventsList)

		result = self.submachines[0].run()
		#self.setOutput(self.submachines[0].getOutput())
		self.outputs.append(event["content"])
		print result
		self.setEventsList(list())
		return result