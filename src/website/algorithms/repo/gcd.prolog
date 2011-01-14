gcd(A,0,A) :- !.
gcd(A,B,R) :- T is A mod B, gcd(B,T,R).
