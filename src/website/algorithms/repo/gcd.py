#!/usr/bin/python

def gcd(a,b):
	if b==0:
		return a
	return gcd(b,a%b)


print gcd(110,10)
print gcd(1407,3441)
print gcd(12,42)
print gcd(3121,73165603)
print gcd(3072,8388608)
