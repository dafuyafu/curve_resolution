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
			glued is the list 

		'''
		self.axis = (x,y)
		self.glued = []

	def glue(self, self_axis_index, aff, aff_axis_index):
		if self.axis[self_axis_index] * aff.axis[aff_axis_index] == 1:
			self.glued.append((self_axis_index, aff, aff_axis_index))
		else:
			raise Exception("Invalid Error: Cannot glue argument affine open")

	def __eq__(self, aff):
		if not isinstance(aff, AffineOpen):
			return NotImplemented
		if self.axis[0] == aff.axis[0] and self.axis[1] == aff.axis[1]:
			return True
		elif self.axis[1] == aff.axis[0] and self.axis[0] == aff.axis[1]:
			return True
		else
			return False

	def __str__(self):
		return "AA(" + str(self.axis[0]) + ", " + str(self.axis[1]) + ")"


class ExceptionalCurve:
	def __init__(self):
		self.divisors = []

	def set(self, affine, ideal):
		self.divisors.append((affine, ideal))

	def __str__(self):
		_text = ""
		for div in self.divisors:
			_text += "{" + str(div[0]) + ", " + str(div[1][0]) + "}, "
		return "ExceptionalCurve(" + _text[:-2] + ")"

	@classmethod
	def intersection(cls, exc1, exc2):
		for d in exc1.divisors:
			for e in exc2.divisors:
				if d[0] == e[0]:
					its = solve([d[1][0], e[1][0]])
					if type(its) == list and len(its) > 0:
						return True
					elif type(its) == dict:
						return True
					else
						pass
		return False