
class Engine(object):

	event = {"id": None,
			 "name": None,
			 "type": None,
			 "content": None}

	verboseType = {"Listing": "report",
				   "Block Track": "track"}

	eventTreatment = {}

	def __init__(self, name):
		self.eventsList = []
		self.name = name
		self.inputs = []
		self.outputs = []

	def setup(self, inputs_, gran, verbOpt):
		self.eventsList = list()
		self.inputs = inputs_
		self.granularity = gran
		self.verboseOptions = verbOpt 

	def readInput(self):
		pass

	def initialEvents(self):
		order = 1
		for input_ in self.inputs:
			new_event = dict(Engine.event)
			new_event["id"] = order
			new_event["type"] = 1
			new_event["content"] = input_
			self.eventsList.append(new_event)
			order += 1
		self.inputs = list()

	def scheduler(self):
		if self.verboseOptions["Event Track"]:
			print "Tratando evento " + str(self.eventsList[0]["type"])
		exec "self.event" + str(self.eventsList[0]["type"]) + "Handler" + "(self.eventsList[0])"

	def run(self):
		self.initialEvents()
		print "Entrou no bloco " + self.name
		while len(self.eventsList) != 0:
			self.scheduler()
		print "Saiu do bloco " + self.name
		self.finalPrint()
		return True


	def blockTrack(self):
		print "\nBlock Track: ",
		if len(self.inputs) == 0:
			print "Leaving ", 
		else:
			print "Entering ",
		print self.name

	def finalPrint(self):
		pass

	def verbose(self):
		for key, value in self.verboseOptions.iteritems():
			if value:
				exec self.verboseAction[key]

	def getOutput(self):
		return self.outputs

