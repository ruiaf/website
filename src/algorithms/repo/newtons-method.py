# newton's method

PRECISION = 0.000000000001

# x1 = x - f(x)/f'(x)
def newthon_method(guess,fn,fn_d):
	while True:
		newguess = guess - ((fn(guess))/(fn_d(guess)))
		if abs(newguess - guess) <= PRECISION: return newguess
		guess = newguess
		print guess

# calculate the square sqrt of a number
# f(x) = X^2 - Number
# f'(x) = 2X
def newton_sqrt(num):
	guess = num/2
	return newthon_method(guess,lambda x: x**2-num,lambda x: 2*x)

newton_sqrt(3214.0)
