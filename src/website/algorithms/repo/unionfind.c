#include <stdio.h>
#include <string.h>

#define N (100)

int dad[N];

/* if apply flag is on, connect two branches of the graph.
 * Returns true if the 2 nodes are connected
 */
int unionfind_slow(int a, int b, int apply) {
	int i=a, j=b;
	/* join a with the topmost parent */
	while (dad[i] > 0 ) i=dad[i];
	/* join b with the topmost parent */
	while (dad[j] > 0 ) j=dad[j];
	/* if to apply, join them */
	if (apply && i!=j) {
		dad[j]=i;
		return 1;
	}
	/* are they in the same tree? */
	return (i==j);
}

/* if apply flag is on, connect two branches of the graph.
 * Returns true if the 2 nodes are connected
 *
 * 1-lets put the best root in every node we transverse
 * 2-when unioning, select the tree with less nodes to
 *   have the other as parent it will keep it balanced.
 *   save the number of noded in the root as neg number
 */
int unionfind(int a, int b, int apply) {
	int t, i=a, j=b;
	/* join a with the topmost parent */
	while (dad[i]>0) i=dad[i];
	/* join b with the topmost parent */
	while (dad[j]>0) j=dad[j];

	/* apply the top most parent to all the nodes in the way*/
	while (dad[a]>0) { t=a; a=dad[a]; dad[t]=i; } 
	/* apply the top most parent to all the nodes in the way*/
	while (dad[b]>0) { t=b; b=dad[b]; dad[t]=i; } 

	if (apply && i!=j) {
		if (dad[j]<dad[i])
			{ dad[j] += dad[i]-1; dad[i]=j; }
		else
			{ dad[i] += dad[j]-1; dad[j]=i; }
		return 1;
	}

	/* are they in the same tree? */
	return (i==j);
}

int main(void) {
	memset(dad,sizeof(dad),0);


	/* lets union some prime numbers */
	unionfind(2,7,1);
	unionfind(3,11,1);
	unionfind(13,7,1);
	unionfind(5,7,1);
	unionfind(2,11,1);
	/* and some non prime */
	unionfind(8,1,1);
	unionfind(6,20,1);
	unionfind(1,6,1);

	printf("%d %d, %d\n", 2,7,unionfind(2,7,0));
	printf("%d %d, %d\n", 5,11,unionfind(5,11,0));
	printf("%d %d, %d\n", 5,8,unionfind(5,8,0));
	printf("%d %d, %d\n", 20,1,unionfind(20,1,0));
	
	return 0;
}
