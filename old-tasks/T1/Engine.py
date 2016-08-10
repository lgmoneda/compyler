
class Engine(object):

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
		pass

	def blockTrack(self):
		print "\nBlock Track: ",
		if len(self.inputs) == 0:
			print "Leaving ", 
		else:
			print "Entering ",
		print self.name