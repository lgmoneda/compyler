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
				if ord(event["content"]) == 10:
					print "line break ",
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
			print '{0: <3}'.format(event["content"].encode('string_escape')), 
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

	def preClassify(self, event):
		if ord(event["content"]) in range(65, 91) or (ord(event["content"]) - 32) in range(65, 91):
				type_ = "letter"
		else:
			if ord(event["content"]) in range(48, 58):
				type_ = "numerical"
			else:
				type_ = "special"

		new_content = dict()
		new_content["value"] = event["content"]
		new_content["type"] = type_
		event["content"] = new_content

	def event1Handler(self, event):
		if self.verboseOptions["Listing"]: self.eventListing(event)
		self.preClassify(event)
		self.outputs.append(event["content"])
		self.eventsList.pop(0)
		return True

