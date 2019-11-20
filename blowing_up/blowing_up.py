from sympy import *
from . import indprt as pr
from . import exceptional_curve as ex

def blowing_up(f):
	x,y = symbols('x,y')
	sing = solve([f, diff(f, x), diff(f, y)])

	# verify whether the polynomial meets the condition
	if not sing[0] == {x: 0, y: 0}:
		# throw an exception
		raise Exception("Invalid Value: the polynomial needs to have only one singular point at the origin.")
	else:
		# process blowing up of the polynomial
		exceptional_set_list = []
		exceptional_set_list.extend(_blowing_up(f))
		for e in exceptional_set_list:
			print(e)

def _blowing_up(f, n=0, axis=[symbols('x'),symbols('y')]):
	var = [symbols('x'),symbols('y')]

	# step 1: define affine open sets and glue them
	affine_open =  [ex.AffineOpen(axis[0], axis[1] / axis[0]),
					ex.AffineOpen(axis[0] / axis[1], axis[1])]

	affine_open[0].glue(affine_open[0].axis[1], affine_open[1], affine_open[1].axis[0])
	affine_open[1].glue(affine_open[1].axis[0], affine_open[0], affine_open[0].axis[1])

	ex_ideal_list = []
	exceptional_list = []
	returned_exceptional_list = []

	# step 2: calculate the strict transforms on affine open subsets defined above
	for t in range(2):
		pr.indprt("on U_" + str(var[t]), n)

		# step 2-1: substitute local variables on each open set
		poly_name = "f_" + str(var[t])
		_f = f
		for s in var:
			if s == var[t]:
				continue
			else:
				_f = _f.subs({s: s * var[t]})

		while(1):
			try:
				_f = exquo(_f, var[t])
			except ExactQuotientFailed:
				break

		pr.indprt(poly_name + " = " + str(_f), n + 1, linebreak=False)
		ex_ideal_list.append((affine_open[t], [var[t]]))

		# step 2-2: decide whether the surface is singular or not with Jacobian criterion
		sing = solve([_f, diff(_f, var[0]), diff(_f, var[1])])
		if sing == []:

			# if nonsingular
			print(" : nonsingular")
			pr.indprt("Exc: V(" + str(var[t]) + ")", n + 1, linebreak=False)

			# verify transversality of strict transformation and exceptional curve
			intersection = solve([_f, var[t]])
			if intersection == []:
				print(": no crossing")
				continue
			elif type(intersection) is list and len(intersection) == 1:
				_g = _f
				for c in var:
					_g = _g.subs({c: c + intersection[0][c]})
				if _g * var[t] == var[0] * var[1] or _g * var[t] == - var[0] * var[1]:
					print(": normal crossing")
				else:
					print(": not normal crossing")
					exceptional_list.extend(_blowing_up(_f, n + 1, axis=[affine_open[t].axis[0], affine_open[t].axis[1]]))
			elif type(intersection) is dict:
				_g = _f
				for c in var:
					_g = _g.subs({c: c + intersection[c]})
				if _g * var[t] == var[0] * var[1] or _g * var[t] == - var[0] * var[1]:
					print(": normal crossing")
				else:
					print(": not normal crossing")
					exceptional_list.extend(_blowing_up(_f, n + 1, axis=[affine_open[t].axis[0], affine_open[t].axis[1]]))
			else:
				print()
				exceptional_list.extend(_blowing_up(_f, n + 1, axis=[affine_open[t].axis[0], affine_open[t].axis[1]]))
		else:
			# if singular
			print(" : singular")
			pr.indprt("Exc: V(" + str(exc) + ")", n + 1)
			pr.indprt("Sing V(" + poly_name + ") = " + str(sing), n + 1)

			# for dim Sing = 0
			if sing[0] == {var[0]: 0, var[1]: 0}:
				pass
			else:
				# translate coordinates to a singular point
				pr.indprt("coordinate translation", n + 1)
				pr.indprt(str(sing[0]) + " --> {x: 0, y: 0}", n + 1)

				for c in var:
					_f = _f.subs({c: c + sing[0][c]})

				pr.indprt(poly_name + " = " + str(_f), n + 1)

			print("")
			exceptional_list.extend(_blowing_up(_f, n + 1, axis=[affine_open[t].axis[0], affine_open[t].axis[1]]))

	# step3: sort ex_ideal_list and define exceptional sets and make them exceptional list
	exceptional_curve = ex.ExceptionalCurve(affine_open)
	exceptional_curve.set_ideal(ex_ideal_list[0][1], ex_ideal_list[1][1])
	exceptional_list.insert(0, exceptional_curve)
	
	return exceptional_list