def indprt(str, n, *, linebreak=True):
	while n > 0:
		print("    ", end="")
		n -= 1
	if linebreak:
		print(str)
	else:
		print(str, end="")