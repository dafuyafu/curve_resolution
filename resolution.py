'''

	Resolution of Curve Singularities
	2019 by dafuyafu

'''
from sympy import *
from blowing_up import blowing_up as bu

if __name__ == '__main__':
	x = symbols('x')
	y = symbols('y')
	f = x ** 34 - y ** 29
	# f = x ** 3 - (x - y) ** 2 # 2,3-cusp with co-tr
	# f = x ** 25 - y ** 19 # 19,25-cusp
	# f = x ** 3 + x ** 2 - y ** 2 # node
	sing = solve([f, diff(f, x), diff(f, y)])
	print("f = " + str(f))
	print("Sing V(f) = " + str(sing))
	print("")
	bu.blowing_up(f)