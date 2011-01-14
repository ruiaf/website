# secant method

PRECISION = 0.000000000001

# x_n+1 = x_n - ((x_n - x_n-1)/(f(x_n)-f(x_n-1)))*f(x_n)
def secant_method(xn0,xn1,fn):
	while True:
		xn2 = xn1 - ((xn1-xn0)/(fn(xn1)-fn(xn0)))*fn(xn1)
		if abs(xn2 - xn1) <= PRECISION: return xn2
		xn0 = xn1
		xn1 = xn2
		print xn2

# calculate the square sqrt of a number
# f(x) = X^2 - Number
def secant_sqrt(num):
	return secant_method(num/2,num/4,lambda x: x**2-num)

secant_sqrt(3214.0)
