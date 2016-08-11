from Engine import Engine

class SemanticEngine(Engine):

	def __init__(self, name):
		super(SemanticEngine, self).__init__(name)

	def event1Handler(self, event):
		self.outputs.append(event["content"])
		self.eventsList.pop(0)
