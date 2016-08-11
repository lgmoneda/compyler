from Engine import Engine


class OuterEngine(Engine):

	def __init__(self, name):
		super(OuterEngine, self).__init__(name)
		self.verboseAction = {"Listing": "self.listing()",
							  "Block Track": "self.blockTrack()"}

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

	def eventListing(self, event):
		print '{0: <5}'.format(event["id"]),
		if self.granularity == "char":
			print '{0: <3}'.format(event["content"]), 
			if ord(event["content"]) in range(65, 91) or (ord(event["content"]) - 32) in range(65, 91):
				print '{0: <10}'.format("letter"),
			else:
				if ord(event["content"]) in range(48, 58):
					print '{0: <10}'.format("numerical"),
				else:
					print '{0: <10}'.format("special"),
			print '{0: <5}'.format(ord(event["content"])),
			print '{0: <5}'.format(hex(ord(event["content"])))
		else:
			print '{0: <3}'.format(event["content"])

	def event1Handler(self, event):
		if self.verboseOptions["Listing"]: self.eventListing(event)
		self.outputs.append(event["content"])
		self.eventsList.pop(0)

