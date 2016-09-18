from Engine import Engine

class BackEngine(Engine):

	def __init__(self, name):
		super(BackEngine, self).__init__(name)

	def event1Handler(self, event):
		self.outputs.append(event["content"])
		self.eventsList.pop(0)
		return True
