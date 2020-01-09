from sympy import *
import networkx as nx
import matplotlib.pyplot as plt
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
		exceptional_curve_list = []
		exceptional_curve_list.extend(_blowing_up(f))
		for e in exceptional_curve_list:
			print(e)

		graph = nx.Graph()
		colors = []
		for e in exceptional_curve_list:
			graph.add_node(exceptional_curve_list.index(e))
			if isinstance(e, ex.NonsingularStrictTransform):
				colors.append("blue")
			else:
				colors.append("red")
			for g in exceptional_curve_list:
				if ex.ExceptionalCurve.intersection(e,g):
					graph.add_edge(exceptional_curve_list.index(e),exceptional_curve_list.index(g))
		
		pos = nx.spring_layout(graph)
		plt.figure(figsize=(6, 6))
		nx.draw_networkx_nodes(graph, pos, node_color = colors)
		nx.draw_networkx_edges(graph, pos)
		plt.axis('off')
		plt.show()

def _blowing_up(f, n=0, current_affine_open=ex.AffineOpen(symbols('x'),symbols('y'))):
	var = [symbols('x'),symbols('y')]

	'''
		# step 1: define affine open sets and glue them
		If is the initial blowing up, i.e. the blowing up of AA(x,y) at the origin, we need two affine_opens which have one affine axis and the other axis is isomorphic to a projective line. For other cases we define affine_opens which have two projective axes.

	'''
	if current_affine_open == ex.AffineOpen(var[0], var[1]):
		affine_open =  [ex.AffineOpen(var[0], var[1] / var[0]),
						ex.AffineOpen(var[0] / var[1], var[1])]
	else:
		affine_open =  [ex.AffineOpen(current_affine_open.axis[0], current_affine_open.axis[1] / current_affine_open.axis[0]),
						ex.AffineOpen(current_affine_open.axis[0] / current_affine_open.axis[1], current_affine_open.axis[1])]

	affine_open[0].glue(1, affine_open[1], 0)
	affine_open[1].glue(0, affine_open[0], 1)

	if current_affine_open.axis[0] == var[0]:
		pass
	else:
		affine_open[0].glue(0, current_affine_open.glued[0]['affine'], 1)

	if current_affine_open.axis[1] == var[1]:
		pass
	else:
		affine_open[1].glue(1, current_affine_open.glued[1]['affine'], 0)

	nonsingular_strict_transform = ex.NonsingularStrictTransform()
	exceptional_curve = ex.ExceptionalCurve()
	exceptional_list = []

	# step 2: calculate the strict transforms on affine open subsets defined above
	for t in range(2):
		pr.indprt("on " + str(affine_open[t]) + ":", n)

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
		exceptional_curve.set(affine_open[t], var[t])

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
			elif type(intersection) is list and len(intersection) == 1:
				_g = _f
				for c in var:
					_g = _g.subs({c: c + intersection[0][c]})
				if _g * var[t] == var[0] * var[1] or _g * var[t] == - var[0] * var[1]:
					print(": normal crossing")
					nonsingular_strict_transform.set(affine_open[t], _f)
				else:
					print(": not normal crossing")
					exceptional_list.extend(_blowing_up(_f, n + 1, current_affine_open=affine_open[t]))
					affine_open[t].detach(t)
					affine_open[t].detach(1-t)
					affine_open[1-t].detach(t)
			elif type(intersection) is dict:
				_g = _f
				for c in var:
					_g = _g.subs({c: c + intersection[c]})
				if _g * var[t] == var[0] * var[1] or _g * var[t] == - var[0] * var[1]:
					print(": normal crossing")
					nonsingular_strict_transform.set(affine_open[t], _f)
				else:
					print(": not normal crossing")
					exceptional_list.extend(_blowing_up(_f, n + 1, current_affine_open=affine_open[t]))
					affine_open[t].detach(t)
					affine_open[t].detach(1-t)
					affine_open[1-t].detach(t)
			else:
				print()
				exceptional_list.extend(_blowing_up(_f, n + 1, current_affine_open=affine_open[t]))
				affine_open[t].detach(t)
				affine_open[t].detach(1-t)
				affine_open[1-t].detach(t)
		else:
			# if singular
			print(" : singular")
			pr.indprt("Exc: V(" + str(var[t]) + ")", n + 1)
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
			exceptional_list.extend(_blowing_up(_f, n + 1, current_affine_open=affine_open[t]))
			affine_open[t].detach(t)
			affine_open[t].detach(1-t)
			affine_open[1-t].detach(t)

	# 現在のリストの中のExcのAffineが自分と貼り合わさってたらもう一個付け足す．
	for t in range(2):
		for exc in exceptional_list:
			for div in exc.divisors:
				for value in div['open'].glued.values():
					if affine_open[t] == value['affine']:
						exceptional_curve.set(div['open'], var[1-t])

	# step3: make an exceptional list
	if nonsingular_strict_transform.divisors == []:
		pass
	else:
		exceptional_list.insert(0, nonsingular_strict_transform)
	exceptional_list.insert(0, exceptional_curve)
	
	return exceptional_list