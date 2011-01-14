/* Rui Ferreira
 * gcc -ansi -Wall -o trie trie.c
 * /

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX ('z'-'a')

/* trie node */
typedef struct trie_t {
  struct trie_t * next[MAX];
  int val;
} trie;

/* allocate memory for node */
trie * new_trie()
{
  trie * t;
  
  t = (trie *) malloc(sizeof(trie));
  t->val = 0;
  memset(t->next, 0, sizeof(t->next));
  
  return t;
}

/* insert word if it doesn't exists, returns word counter */
int trie_insert(trie * t, char *s)
{
  if(*s)
    {
      if(t->next[*s-'a'] == NULL)
	t->next[*s-'a'] = new_trie();
      return trie_insert(t->next[*s-'a'], s+1);
    }
  
  return ++t->val;
}

/* search word, returns word counter */
int trie_search(trie *t, char *s)
{
  if(*s)
    {
      if(t->next[*s-'a'] == NULL)
	return 0;
      return trie_search(t->next[*s-'a'], s+1);
    }
   
  return t->val;
}

/* deallocate mem */
void free_trie(trie *t)
{
  int i;
  if (t!=NULL)
    {
      for (i=0;i<MAX;i++)
	free_trie(t->next[i]);
      free(t);
    }
}


int main(void)
{
  trie *t;
  
  t = new_trie();
  printf("Added %s %d\n","texta",trie_insert(t,"texta"));
  printf("Added %s %d\n","textb",trie_insert(t,"textb"));
  printf("Added %s %d\n","texta",trie_insert(t,"texta"));
  printf("Searched %s %d\n","texta",trie_search(t,"texta"));
  printf("Searched %s %d\n","textc",trie_search(t,"textc"));
  free_trie(t);

  return 0;
}

