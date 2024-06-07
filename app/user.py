
class User(dict):
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymus(self):
		return True
	def get_id(self):
		return str(self['user_id'])
	def userid(self, key):
		self.id = key