class Engine(object):
	"""The basic event based Engine.

	This class contains the basic structure of a event driven engine, witch
	include a method to create the initial events from the input, 
	a scheduler that addresses the event treatment to the right handler and
	a run routine, that basically runs the engine until it treats all its 
	events.

	Class Attributes:
		event: the model considered to represent an event. The name shall
			help us to identify the different kind of events for many types
			of engines. The content is the data itself. The type is used to
			address the right handler and the id does not have a key role
			yet.
		verboseType: indicates what kind of verbose a certain field is.
	Attributes:
		eventList: a list of events to be treated. New events are appended 
			and we pop out the finished ones.
		name: engine identifier.
		inputs: the engine input. They'll be transformed into initial events
			by the right method.
		outputs: the processed inputs.  
	Args:
		name: The engine/block name.
	"""

	event = {"id": None,
			 "name": None,
			 "type": None,
			 "content": None}

	verboseType = {"Listing": "report",
				   "Block Track": "track"}

	def __init__(self, name):
		self.eventsList = []
		self.name = name
		self.inputs = []
		self.outputs = []

	def setup(self, inputs_, gran, verbOpt):
		"""Setup the engine

		Receives specific characteristics from a certain simulation, such as 
		the input to be processed, the granularity to be considered and the 
		verbose options. Resets the old output.

		Args:
			inputs_: A list containing the content to be processed.
			gran: A string indicating the granularity we will work with.
			verbOpt: A dict with the verbose options.
		Returns:
			None
		"""
		self.eventsList = list()
		self.inputs = inputs_
		self.outputs = list()
		self.granularity = gran
		self.verboseOptions = verbOpt 

	def readInput(self):
		pass

	def initialEvents(self):
		"""Reads the input and create the first events

		The starter function to a event-based simulation. We need to define the first
		events to populate the event list. It read each content in the input_ and turns
		it into an event. We need to take care with the case where the self.inputs is,
		in fact, a single input.

		Returns:
			None
		"""
		order = 1
		if type(self.inputs) == list:
			for input_ in self.inputs:
				new_event = dict(Engine.event)
				new_event["id"] = order
				new_event["type"] = 1
				new_event["content"] = input_
				self.eventsList.append(new_event)
				order += 1
		else:
			new_event = dict(Engine.event)
			new_event["id"] = order
			new_event["type"] = 1
			new_event["content"] = self.inputs
			self.eventsList.append(new_event)

		self.inputs = list()

	def scheduler(self):
		"""Addresses the right handler to the events.

		The engine should treat all the events. We get the first in the list
		and execute the right handler for it.

		Returns:
			None
		"""
		if self.verboseOptions["Event Track"]:
			print "Treating event " + str(self.eventsList[0]["type"])
		exec "self.event" + str(self.eventsList[0]["type"]) + "Handler" + "(self.eventsList[0])"

	def run(self):
		"""Run the engine.

		Put the engine in action. While there's events in the list to be treated, run 
		the scheduler. When it finishes, call a report function. It informs too the 
		entrance and exit from the block/engine.

		Returns:
			A boolean indicating or not a successful running.
		"""
		if self.verboseOptions["Block Track"]: self.blockTrack()
		self.initialEvents()
		#print "Entrou no bloco " + self.name
		while len(self.eventsList) != 0:
			self.scheduler()
		#print "Saiu do bloco " + self.name
		if self.verboseOptions["Block Track"]: self.blockTrack()
		self.finalPrint()
		return True

	def blockTrack(self):
		"""Prints the block track

		Prints the entrance and exit from blocks/engines when this verbose is 
		enabled.

		Returns:
			None
		"""
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

