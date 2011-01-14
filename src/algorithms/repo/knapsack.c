/* Rui Ferreira, Dynamic Programing
 * 
 */
#include <stdio.h>
#include <string.h>

/* N types of items */
#define N (5)
/* capacity of the knapsack */
#define M (17)

int size[N+1] = {0,3,4,7,8,9};
int val[N+1] = {0,4,5,10,11,13};
int best[M+1];
int cost[M+1];

int main(void) {
	int i,j;
		
	memset(best,sizeof(best),0);
	memset(cost,sizeof(cost),0);

	for (j=1;j<=N;j++)
		for (i=1;i<=M;i++)
			if (i>=size[j] && (cost[i]<=(cost[i-size[j]]+val[j]))) {
				cost[i]=cost[i-size[j]]+val[j];
				/* best - used to recover the contents of the knapsack */
				best[i]=j;
			}

	printf("%d ->",cost[M]);

	i=M;
	while ( i!=0) {
		printf(" %d",size[best[i]]);
		i = i-size[best[i]];
	}
	putchar('\n');
	

	return 0;
}
