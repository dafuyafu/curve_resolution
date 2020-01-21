'''

	In this module, we define the geometric classes, AffineOpen, ExceptionalCurve and NonsingularStrictTransform.

'''

from sympy import *

class AffineOpen:

	'''
		class AffineOpen:
		AffineOpen is the class which represents an affine open subset of A2.

		axis: tuple of labels of x-axis and y-axis of the affine open which is isomorphic A2. The constructor arguments are monomial rational functions.
		glued: dictionary 

		affine_open.axis = (u, v) # tuple
		affine_open.glued = {0: {affine: AA(u, v), 'axis': 1}, 1: {'affine': AA(w, t), 'axis': 0}} # dictionary

	'''

	def __init__(self, x, y):
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
			pass

	def __eq__(self, aff):
		if not isinstance(aff, AffineOpen):
			return NotImplemented
		if set(self.axis) == set(aff.axis):
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
			_text += "{" + str(div['ideal']) + ", " + str(div['open']) + "}, "
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
			_text += "{" + str(div['ideal']) + ", " + str(div['open']) + "}, "
		return "NonsingularStrictTransform(" + _text[:-2] + ")"