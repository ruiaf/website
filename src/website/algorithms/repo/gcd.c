#include <stdio.h>

int gcd(int a,int b) {
	if (!b) return a;
	return gcd(b,a%b);
}

int main(void) {

printf("%d\n",gcd(110,10));
printf("%d\n",gcd(1407,3441));
printf("%d\n",gcd(12,42));
printf("%d\n",gcd(3121,73165603));
printf("%d\n",gcd(3072,8388608));

return 0;
}
