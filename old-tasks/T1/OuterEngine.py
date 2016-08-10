from Engine import Engine

class OuterEngine(Engine):

	def __init__(self, name):
		super(OuterEngine, self).__init__(name)
		print "funciona"

	def setup(self, inputs_, gran, verbOpt):
		self.eventsList = list()
		self.inputs = inputs_
		self.granularity = gran
		self.verboseOptions = verbOpt 

	def input(self):
		pass

	def run(self):

		self.verboseAction = {"Listing": "self.listing()",
							  "Block Track": "self.blockTrack()"}
		self.blockTrack()
		self.initialEvents()
		for key, value in self.verboseOptions.iteritems():
			if value:
				exec self.verboseAction[key]

	def listing(self):
		print "\n"
		for event in self.eventsList:
			print str(event["id"]) + " ",
			if self.granularity != "char": 
				print event["content"]
			else:
				print event["content"] + " ",

				if ord(event["content"]) in range(65, 91) or (ord(event["content"]) - 32) in range(65, 91):
					print "letter ",
				else:
					if ord(event["content"]) in range(48, 58):
						print "numerical ",
					else:
						print "special ",
				print str(ord(event["content"])) + " ",
				print hex(ord(event["content"]))

