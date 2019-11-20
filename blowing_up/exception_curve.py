'''

	In this module, we define the geometric classes. 

	# class AffineOpen
		self.axis: list of labels of x-axis, y-axis and z-axis of the affine open which is isomorphic A3. The constructor arguments are monomial rational functions.

		def glue(aff, t, s):
			aff: an AffineOpen instance which is glued to self.
			self_axis: an axis of self
			aff_axis: an axis of aff

'''


from sympy import *

class AffineOpen:
	def __init__(self, x, y):
		self.axis = [x,y]
		self.glued = []

	def glue(self, self_axis, aff, aff_axis):
		if self_axis in self.axis and aff_axis in aff.axis and self_axis * aff_axis == 1:
			self.glued.append((self.axis.index(self_axis), aff, aff.axis.index(aff_axis)))
			self.glued.append((aff.axis.index(aff_axis), self, self.axis.index(self_axis)))
		else:
			raise Exception("Invalid Error: Cannot glue argument affine open")

	def __str__(self):
		return "A(" + str(self.axis[0]) + ", " + str(self.axis[1]) + ")"


class ExceptionCurve:
	def __init__(self, af):
		self.affine_open = af
		self.is_empty = True
		self.ideal = []

	def set_ideal(self, exc_x, exc_y):
		self.ideal.append(exc_x)
		self.ideal.append(exc_y)
		self.is_empty = False

	def has_intersection(self, exc):
		if self.is_empty or exc.is_empty:
			raise Exception("Error")
		else:
			pass
			# 後で書く

	def __str__(self):
		if self.is_empty:
			return "self is Empty."
			
		'''
			Caution!
			Following sentence "self.ideal[0][0] ~ " operates correctly only for curves, so it must be fixed to be suitable for arbitary hypersurface.

		'''
		_x = self.ideal[0][0].subs({symbols('x'): self.affine_open[0].axis[0], symbols('y'): self.affine_open[0].axis[1]})
		_y = self.ideal[1][0].subs({symbols('x'): self.affine_open[1].axis[0], symbols('y'): self.affine_open[1].axis[1]})
		return "ExceptionCurve({" + str(self.affine_open[0]) + ", " + str(_x) + "}, {" + str(self.affine_open[1]) + ", " + str(_y) + "})"