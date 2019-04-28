#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "PQ.h"


typedef struct PQNode{ // Linked list representation of PQ
  ItemPQ PQitem;
  struct PQNode *next;
}PQNode;

typedef struct PQRep{
  PQNode *first;
  PQNode *last;
}PQRep;

//Helper function
// static void reverse(PQnode *node);
// static void rearrange(PQNode *node);
//static void deletePQNode(PQNode **first, int position);
static void deletePQNode(struct PQNode* pos);
static void insertPQNode(PQ q, struct PQNode* new);
static int insertPQNodeFifoFirst(struct PQNode* prev, struct PQNode* pos, struct PQNode* new);
static int insertPQNodeFifo(struct PQNode* prev, struct PQNode* pos, struct PQNode* new);





PQ newPQ(){

  PQRep *temp = malloc(sizeof *temp);
  *temp = (PQRep){ .first = NULL, .last = NULL};
  return temp;

}
/*
Node* newNode(int d, int p)
{
    Node* temp = (Node*)malloc(sizeof(Node));
    temp->data = d;
    temp->priority = p;
    temp->next = NULL;

    return temp;
}*/

void  addPQ(PQ q, ItemPQ item){

  assert(q != NULL);
  struct PQNode *new = malloc (sizeof *new);
  assert (new != NULL);
  *new = (PQNode){ .PQitem.value = item.value,.PQitem.key = item.key, .next = NULL};

  //Check if item with key is already in list
  for(PQNode *curr = q->first; curr != NULL; curr = curr->next){
    if(curr->PQitem.key == item.key){
      curr->PQitem.value = item.value;
      return;
    }
  }

  insertPQNode(q, new);

}


/* Removes and returns the item (ItemPQ) with smallest 'value'.
   For items with equal 'value', observes FIFO.
   Returns null if this queue is empty.
*/

ItemPQ dequeuePQ(PQ q){

  assert (q != NULL);
  assert (q->first != NULL);
  PQNode* temp = q->first;
  ItemPQ it = temp->PQitem;
  q->first = q->first->next;
  free(temp);

  return it;

}

/* Removes and returns the item (ItemPQ) with smallest 'value'.
   For items with equal 'value', observes FIFO.
   Returns null if this queue is empty.
   */
void  updatePQ(PQ q, ItemPQ it){

 assert(q != NULL);
 struct PQNode *curr;
 ItemPQ temp;
 curr = q->first;
 

 while (curr !=NULL) {
   if(curr->PQitem.key == it.key){
     //Create temporary item to add
     temp = curr->PQitem;
     temp.value = it.value;
     temp.key = it.key;

     // //Delete old node
     deletePQNode(curr);

     // Reinsert new PQNode
     addPQ(q, temp);

     return;
   }
   curr = curr->next;

 }
 return;
}

int PQEmpty(PQ q){
  if (q->first == NULL)
    return 1;
  else
    return 0;
}

void showPQ(PQ q){


  for(struct PQNode *curr = q->first; curr != NULL; curr = curr->next){

    printf("List Value: %d List Key: %d\n",curr->PQitem.value , curr->PQitem.key);
  }

  return;
}

void freePQ(PQ q){

  for(struct PQNode *curr = q->first; curr != NULL; curr = curr->next){
       curr->PQitem.value = 0;
       curr->PQitem.key = 0;
       curr->next = NULL;
       free(curr);
  }
  q->first = NULL;
  q->last = NULL;
  free(q);
  return;
}

static void deletePQNode(struct PQNode* pos)
{
    if (pos == NULL) // If linked list is empty
        return;

    else {
        struct PQNode* temp = pos->next;

        // Copy data of the next node to current node
        pos->PQitem.value = pos->next->PQitem.value;
        pos->PQitem.key = pos->next->PQitem.key;
        pos->PQitem = pos->next->PQitem;

        // Perform conventional deletion
        pos->next = pos->next->next;

        free(temp);
    }
    return;
}

//Return 1 is successful, 0 if unsuccessful
static void insertPQNode(PQ q, struct PQNode* new){

 struct PQNode *curr, *prev;
// Cases that don't need FIFO

  //Empty list
  if(q->first == NULL){
    q->first = new;
    q->last = new;
  }

  //Less than value of first
  else if(new->PQitem.value < q->first->PQitem.value){

    new->next = q->first;
    q->first = new;
  }

  //Greater or equal than value of last
  else if (new->PQitem.value >= q->last->PQitem.value) {
 		// largest value case
 		q->last->next = new;
 		q->last = new;
   }

//Cases that need FIFO

  //Equal to first
  else if (new->PQitem.value == q->first->PQitem.value){
    insertPQNodeFifoFirst(q->first, q->first, new);
  }

  //Middle Case
  else {
    prev = q->first;
    curr = q->first->next;
    insertPQNodeFifo(prev,curr,new);
  }

}

static int insertPQNodeFifoFirst(struct PQNode* prev, struct PQNode* pos, struct PQNode* new){

  PQNode *curr;
  curr = pos;

  if(curr->PQitem.value == new->PQitem.value){
    prev = curr;
    curr = curr->next;
    insertPQNodeFifoFirst(prev, curr, new);
  }
  else if (curr->PQitem.value > new->PQitem.value){

    prev->next = new;
    new->next = curr;
    return 1;

  }
  else
  // Error
    return -1;

  return -1;


}

static int insertPQNodeFifo(struct PQNode* prev, struct PQNode* pos, struct PQNode* new){

  PQNode *curr;
  curr = pos;

  if(curr->PQitem.value == new->PQitem.value){
    prev = curr;
    curr = curr->next;
    insertPQNodeFifo(prev, curr, new);
  }
  else if (new->PQitem.value > curr->PQitem.value){
    prev = curr;
    curr = curr->next;
    insertPQNodeFifo(prev, curr, new);
  }
  else if (curr->PQitem.value > new->PQitem.value){

    prev->next = new;
    new->next = curr;
    return 1;

  }
  else // Error
    return -1;

  // else {
  //  curr = q->first;
  //  while (curr && new->PQitem.value > curr->PQitem.value) {
  //    prev = curr;
  //    curr = curr->next;
  //  }
  //  new->next = curr;
  //  prev->next = new;
  //  }


  return -1;

}

/*
static void deletePQNode(PQNode **first, int position){

  if(*first == NULL)
    return;

  struct PQNode* temp = *first;

  if(position == 0)
  {
    *first = temp->next;
    free(temp);
    return;
  }

  for (int i = 0; temp != NULL && i < position-1; i++)
    temp = temp->next;

  if (temp == NULL || temp->next == NULL)
    return;

  struct PQNode *next = temp->next->next;

  free(temp->next);
  temp->next = next;

}
*/
/*
static void reverse(PQNode *first){

assert(q != NULL);
struct PQNode *curr = *first, *prev = NULL, *next;


while (curr){
  next = curr->next;
  curr->next = prev;
  prev = curr;
  curr=next;
}
*first = prev;
}

static void rearrange(PQNode *first){
  struct PQNode *slow = *first, *fast = *slow->next;
  while (fast ** fast->next)
  {
    slow = slow->next;
    fast = fast->next->next;
  }

  struct PQNode *first1 = *first, *first2 = slow->next;
  slow->next = NULL;

  reverse(&first2);

  struct PQNode *new = malloc (sizeof *new);
  *new = (PQNode){ .PQitem.value = 0, .PQitem.key = 0, .next = NULL};

  struct PQNode *curr = *first;
  while (first1 || first2)
  {
    if (first1)
    {
      curr->next = first1;
      curr = curr->next;
      first1 = first1->next;
    }

    if(first2)
    {
      curr->next = first2;
      curr = curr->next;
      first2 = first2->next;
    }


  }
  *first = (*first) ->next;

}
*/

/*
void  addPQ(PQ q, ItemPQ item){

  assert(q != NULL);
  struct PQNode *curr, *prev, *tempFifo;

  struct PQNode *new = malloc (sizeof *new);
  assert (new != NULL);
  *new = (PQNode){ .PQitem.value = item.value,.PQitem.key = item.key, .next = NULL};

  //Check if item with key is already in list
  for(PQNode *curr = q->first; curr != NULL; curr = curr->next){
    if(curr->PQitem.key == item.key){
      curr->PQitem.value = item.value;
      return;
    }
  }


  if(q->first == NULL){
    q->first = new;
    q->last = new;
  }
  else if(new->PQitem.value < q->first->PQitem.value){

    new->next = q->first;
    q->first = new;
  }

  else if(new->PQitem.value == q->first->PQitem.value){
    q->first->next = new;
    new->next = q->first->next->next;
  }

 else if (new->PQitem.value >= q->last->PQitem.value) {
		// largest value case
		q->last->next = new;
		q->last = new;
  }

 else {
  curr = q->first;
  while (curr && new->PQitem.value > curr->PQitem.value) {
    prev = curr;
    curr = curr->next;
  }
  new->next = curr;
  prev->next = new;
  }
}*/
