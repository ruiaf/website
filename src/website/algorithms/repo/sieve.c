/* Rui Ferreira
 * gcc -ansi -Wall -lm -o prime prime.c
 */

#include <stdio.h>
#include <string.h>
#include <math.h>

/* find all primes until N, think big */
#define N 20000

/* create an array to mark if a number is prime */
char isprime[N];

void sieve() {
	unsigned long long int i,j;
	
	/* mark all numbers as prime */
	memset(isprime,1,sizeof(isprime));
	isprime[0]=0;
	isprime[1]=0;

	/* we only need to test until the sqrt. 
 		if there is a bigger factor than this,
		there must also be a smaller one that is also multiple */
	long long unsigned sq = (long long unsigned) sqrt(N);
	for (i=2;i<=sq;i++)
		if (isprime[i]) /* if number is prime, mark multiples as non-prime */
			for (j=i*i;j<N;j+=i)
				if (isprime[j]) /*faster to check than writing multiple times*/
					isprime[j]=0;
}

/* test if number is prime, it would be faster to make a list of primes first */
int isp(long long unsigned i) {
	long long unsigned j;

	int sq = (int) sqrt(i);
	for (j=0;j<=sq;j++)
		if (isprime[j] && i%j==0) /* if the number is divisible by j */
			return 0; /* then it's not prime */

	return 1;
}

int main(void)
{
	long long unsigned i;

	sieve();

	/* Now it's possible to test primality until N^2 */
	for (i=0;;i++) {
		if ((i<N && isprime[i]) || (i>=N && isp(i))) 
			printf("%llu\n",i);
	}
			
	return 0;
}
