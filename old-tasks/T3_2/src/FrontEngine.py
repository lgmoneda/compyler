from Engine import Engine

class FrontEngine(Engine):

	def __init__(self, name):
		super(FrontEngine, self).__init__(name)
	
	def event1Handler(self, event):
		self.outputs.append(event["content"])
		self.eventsList.pop(0)
