'''

	Resolution of Curve Singularities
	2019 by dafuyafu

'''
from sympy import *
from blowing_up import blowing_up as bu
import networkx as nx

if __name__ == '__main__':
	x = symbols('x')
	y = symbols('y')
	# f = x ** 2 * (x - 1) - y ** 2
	f = x ** 3 + x * y ** 3
	sing = solve([f, diff(f, x), diff(f, y)])
	print("f = " + str(f))
	print("Sing V(f) = " + str(sing))
	print("")
	bu.blowing_up(f)