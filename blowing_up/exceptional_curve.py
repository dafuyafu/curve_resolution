'''

	In this module, we define the geometric classes. 

'''


from sympy import *

class AffineOpen:
	'''
		class AffineOpen
		axis: list of labels of x-axis and y-axis of the affine open which is isomorphic A2. The constructor arguments are monomial rational functions.

		def glue(aff, t, s):
			aff: an AffineOpen instance which is glued to self.
			self_axis: an axis of self
			aff_axis: an axis of aff

	'''

	def __init__(self, x, y):

		'''
			axis has labels of axes of affine open set as rational function.
			glued is the dictionary which has the data of glued affine open sets.

			affine_open.axis = (u, v) # tuple
			affine_open.glued = {0: {affine: AA(u, v), 'axis': 1}, 1: {'affine': AA(w, t), 'axis': 0}} # dictionary

		'''
		self.axis = (x,y)
		self.glued = {}

	def glue(self, self_key, aff, aff_key):
		if self.axis[self_key] * aff.axis[aff_key] == 1:
			self.glued[self_key] = {'affine': aff, 'axis': aff_key}
		else:
			raise Exception("Invalid Error: Cannot glue argument affine open")

	def detach(self, key):
		if key in self.glued:
			self.glued.pop(key)
		else:
			print('Not glued')

	def __eq__(self, aff):
		if not isinstance(aff, AffineOpen):
			return NotImplemented
		if self.axis[0] == aff.axis[0] and self.axis[1] == aff.axis[1]:
			return True
		elif self.axis[1] == aff.axis[0] and self.axis[0] == aff.axis[1]:
			return True
		else:
			return False

	def __str__(self):
		return "AA(" + str(self.axis[0]) + ", " + str(self.axis[1]) + ")"


class ExceptionalCurve:
	def __init__(self):
		self.divisors = []

	def set(self, affine, ideal):
		self.divisors.append({'open': affine, 'ideal': ideal})

	def __str__(self):
		_text = ""
		for div in self.divisors:
			_text += "{" + str(div['open']) + ", " + str(div['ideal']) + "}, "
		return "ExceptionalCurve(" + _text[:-2] + ")"

	@classmethod
	def intersection(cls, exc1, exc2):
		for d in exc1.divisors:
			for e in exc2.divisors:
				if d['open'] == e['open']:
					_intersection = solve([d['ideal'], e['ideal']])
					if type(_intersection) == list and len(_intersection) > 0:
						return True
					elif type(_intersection) == dict:
						return True
					else:
						pass
		return False

class NonsingularStrictTransform(ExceptionalCurve):
	def __str__(self):
		_text = ""
		for div in self.divisors:
			_text += "{" + str(div['open']) + ", " + str(div['ideal']) + "}, "
		return "NonsingularStrictTransform(" + _text[:-2] + ")"