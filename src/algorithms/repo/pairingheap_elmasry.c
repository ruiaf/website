#include <stdlib.h>
#include <math.h>

/* A growable array would suit here */
#define MAX_INSERTION_BUFFER_SIZE (10000000)
#define MAX_POOL_SIZE (MAX_INSERTION_BUFFER_SIZE)

typedef struct heap_node {
    struct heap_node *parent;
    struct heap_node *next_sibling;
    struct heap_node *previous_sibling;
    struct heap_node *first_child;
    struct heap_node *last_child;
	int value;
    int n_subtrees;
} heap_node;

typedef struct heap {
    heap_node * root;
    heap_node *insertion_buffer[MAX_INSERTION_BUFFER_SIZE];
    int insertion_buffer_size;
    heap_node *pool[MAX_POOL_SIZE];
    int pool_size;
    heap_node *minimum;
    int n_elements;
} heap;

/***********************************************
 *
 * PRIVATE FUNCTIONS 
 *
 ***********************************************/

/* link two node trees. AKA meld*/
heap_node* heap_node_link(heap_node *small, heap_node *big) {   
    heap_node *tmp;
    
    if (!small) return big;

    if (small->value > big->value) {
        tmp=small; small=big; big=tmp;
    }

    big->parent = small; /* small becomes the partent of big */
    if (small->first_child) { /* if small has children */
        big->next_sibling = small->first_child; /* big has a new sibling */
        big->next_sibling->previous_sibling = big; /* big is the new sibling of someone*/
    } else { /* big is to be only child */
        small->last_child = big; /* big is the last child of small */
    }
    small->first_child = big; /* big is the first child of small */

    return small;
}

/* isolate node from parent and siblings */
void heap_node_isolate(heap_node *node) {
    heap_node *prev_tmp,*next_tmp;

    prev_tmp = node->previous_sibling;
    next_tmp = node->next_sibling;

    /* remove */
    node->previous_sibling = NULL;
    if (prev_tmp) prev_tmp->next_sibling=next_tmp;
    else if (node->parent) node->parent->first_child=next_tmp;

    node->next_sibling=NULL;
    if (next_tmp) next_tmp->previous_sibling=prev_tmp;
    else if (node->parent) node->parent->last_child=prev_tmp;

    node->parent=NULL;
}

/* create a new node */
heap_node* heap_node_new(int value) {
    heap_node *h;

    h = (heap_node*)malloc(sizeof(heap_node));
    /* if you want speed, use memset instead */
    h->parent = NULL;
    h->previous_sibling = NULL;
    h->next_sibling = NULL;
    h->first_child = NULL;
    h->last_child = NULL;
    h->value = value;
    return h;
}

/* free tree of the node */
void heap_node_free(heap_node *h) {
    if (!h)
        return;
    heap_node_free(h->next_sibling);
    heap_node_free(h->first_child);
    free(h);
}

/* print node */
void heap_node_print(heap_node *n) {
    if (!n)
        return;
    printf(">%d<\n",n->value);
    heap_node_print(n->first_child);
    heap_node_print(n->next_sibling);
}

/* print heap */
void heap_print(heap *h) {
    int i;

    puts("root");
    heap_node_print(h->root);

    puts("insertion buffer");
    for (i=0;i<h->insertion_buffer_size;i++) {
        printf("node %d\n:",i);
        heap_node_print(h->insertion_buffer[i]);
    }

    puts("pool");
    for (i=0;i<h->pool_size;i++)
        heap_node_print(h->pool[i]);
}

/* compare two heap nodes, used while combining the pool */
int heap_node_cmp(const void *a, const void *b) {
    heap_node *ha,*hb;
    ha = (heap_node *)a;
    hb = (heap_node *)b;

    return (hb->value)-(ha->value);
}

/* combine heap */
void heap_combine(heap *hp) {
    heap_node *tmp;
    int i,j,next;

    /* multipass of heap_node_link in pairs of the insertion buffer, 1st and 2nd, 3rd and 4th, ...*/
    while (hp->insertion_buffer_size>1) {
        i=0;
        next=0;
        while(next < hp->insertion_buffer_size)
        {
            if (next+1==hp->insertion_buffer_size)
                hp->insertion_buffer[i] = hp->insertion_buffer[next];
            else
                hp->insertion_buffer[i] = heap_node_link(hp->insertion_buffer[next],hp->insertion_buffer[next+1]);
            i++;
            next +=2;
        }
        hp->insertion_buffer_size=i;

        i=0;
        j=hp->insertion_buffer_size-1;
        /* reverse items */
        while (i<=j) {
            tmp = hp->insertion_buffer[i];
            hp->insertion_buffer[i] = hp->insertion_buffer[j];
            hp->insertion_buffer[j]=tmp;
            i++;
            j--;
        }

    }

    if (hp->pool_size) {
        qsort(hp->pool,hp->pool_size, sizeof(heap_node*),heap_node_cmp);

        while(hp->pool_size-->1) {
            hp->pool[hp->pool_size-1] = heap_node_link(hp->pool[hp->pool_size-1],hp->pool[hp->pool_size]);
        }
    }

    if (hp->pool_size)
        hp->root = heap_node_link(hp->root,hp->pool[--hp->pool_size]);
    if (hp->insertion_buffer_size)
        hp->root = heap_node_link(hp->root,hp->insertion_buffer[--hp->insertion_buffer_size]);
}

/***********************************************
 *
 * PUBLIC FUNCTIONS 
 *
 ***********************************************/

/* free heap */
void heap_free(heap *h) {
    if (h->n_elements) {
        heap_node_free(h->root);
        while (h->pool_size) {
            heap_node_free(h->pool[--(h->pool_size)]);
        }
        while (h->insertion_buffer_size) {
            heap_node_free(h->insertion_buffer[--(h->insertion_buffer_size)]);
        }
    }
    free(h);
}

/* get min value */
int heap_min(heap *h){
    return h->minimum->value;
}

/* decrease the value of the node */
void heap_decrease_key(heap *h, heap_node *node, int delta) {
    heap_node *node_first_child;
    node->value -= delta;

    if (node->value < h->minimum->value) {
        h->minimum = node;
    }

    /* left most sub child takes place of node */
    if (node!=h->root) {
        node_first_child = node->first_child;
        if (node_first_child) {
            heap_node_isolate(node_first_child);
            node->first_child->parent = node->parent;
            node->first_child->next_sibling = node->next_sibling;
            node->first_child->previous_sibling = node->previous_sibling;

            if (node->next_sibling) {
                node->next_sibling->previous_sibling = node_first_child;
            } else {
                node->parent->last_child = node_first_child;
            }

            if (node->previous_sibling) {
                node->previous_sibling->next_sibling = node_first_child;
            } else {
                node->parent->first_child = node_first_child;
            }
        } else {
            heap_node_isolate(node);
        }
    }

    /* add the rest of node's subtrees to the pool as standalone trees */
    while (node->first_child) {
        h->pool[h->pool_size++] = node->first_child;
        heap_node_isolate(node->first_child);
    }

    if (h->pool_size>=log2(h->n_elements))
        heap_combine(h);
}

/* insert element to the heap */
heap_node *heap_insert(heap *h,int value) {
    heap_node * hn = heap_node_new(value);
    h->insertion_buffer[(h->insertion_buffer_size)++] = hn;
    if (h->minimum==NULL || value < h->minimum->value) {
        h->minimum = hn;
    }
    h->n_elements++;
    return hn;
}

/* delete min value. classic two-pass */
void heap_delete_min(heap *hp) {
    heap_node *a,*b,*next_tmp,*new_root=NULL,*h;

    heap_combine(hp);
    h = hp->root;

    /* two-pass merge */
    /* heap_node_link in pairs, 1st and 2nd, 3rd and 4th, ...*/
    a = h->first_child;
    while(a!=NULL)
    {
        next_tmp=NULL;
        b = a->next_sibling;
        heap_node_isolate(a);
        if (b) {
            next_tmp=b->next_sibling;
            heap_node_isolate(b);
            a = heap_node_link(a,b);
        }
        h = heap_node_link(h,a);
        a = next_tmp;
    }

    /* attach all to the oldest one */
    a = h->first_child;
    while(a!=NULL)
    {
        b = a->next_sibling;
        if (!b) break;
        heap_node_isolate(a);
        heap_node_isolate(b);
        a = heap_node_link(a,b);
        h = heap_node_link(h,a);
    }

    if (h->first_child) {
        new_root = h->first_child;
        h->first_child->parent=NULL;
    }

    free(h);
    hp->n_elements--;
    hp->root = new_root;
    hp->minimum= new_root;
}

/* create a new heap */
heap * heap_new(void) {
    heap *h;
    h = (heap*)malloc(sizeof(heap));
    h->root = NULL;
    h->insertion_buffer_size=0;
    h->pool_size=0;
    h->minimum=NULL;
    h->n_elements=0;

    return h;
}

/* meld two heaps */
heap * heap_meld(heap *small, heap *big) {
    heap *tmp;

    if (!small->minimum)
        return big;
    if (!big->minimum)
        return small;

    if (small->minimum->value > big->minimum->value) {
        tmp=small; small=big; big=tmp;
    }

    heap_combine(small);
    big->pool[big->pool_size++]=small->root;
    if (small->root->value < big->minimum->value) {
        big->minimum = small->root;
    }
    free(small);

    return big;
}
