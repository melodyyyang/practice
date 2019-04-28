// Dijkstra ADT interface for Ass2 (COMP2521)
#include "Dijkstra.h"
#include "PQ.h"
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <limits.h> //library for INT_MAX

typedef ShortestPaths *sp;

static void addPred(sp s, int index, Vertex v);

//add visited vertex v to the pred list of i
static void addPred(sp s, int i, Vertex v) {
    PredNode *new = malloc(sizeof(PredNode));   //allocate memory for prednode
    new->v = v; //initialised the new node
    new->next = NULL;
    if (s->pred[i] == NULL) {   //if the pred list is empty
        s->pred[i] = new;   //add the new pred node to the empty list
    } else {
        PredNode *curr = s->pred[i];    //create another node for pred list
        while (curr->next != NULL) {    //go through every node in the list
            if (curr->v == v) return;   //if vertex v is already in the list, return
            curr = curr->next;
        }
        curr->next = new;   //insert the new node at the end of list
    }
}

//find all shortestpaths for v
ShortestPaths dijkstra(Graph g, Vertex v) {

    sp throwAway = malloc(sizeof(ShortestPaths));   //allocate memory for the shortestpaths struct
    throwAway->noNodes = numVerticies(g);   //initialised the new shortestpaths
    throwAway->src = v;
    throwAway->dist = malloc(throwAway->noNodes*sizeof(int));   //allocate the memory for distance array
    throwAway->pred = malloc(throwAway->noNodes*sizeof(PredNode*)); //allocate the memory for pred node array
    int i;
    for (i = 0; i < throwAway->noNodes; i++){   //go through every node
        throwAway->pred[i]= NULL;   //initialised the pred node array to NULL
        throwAway->dist[i]= INT_MAX;    //initialised the distance array to infinity
    }
   
    throwAway->dist[v] = 0; //the distance form v to v is 0
    ItemPQ *item = malloc(sizeof(ItemPQ));  //allocate the memory for pqitem
    item->key = v;  //initialised the key of item to given vertex
    item->value = 0;    //set the value of item to 0
    PQ q = newPQ(); //created an new pq by using the function in pq.c
    addPQ(q,*item); //add the new item to pq
    
    while(PQEmpty(q) == 0){ //check pq is not empty
        ItemPQ temp = dequeuePQ(q); //created an itempq node for the largest node in pq
        AdjList out = outIncident(g,temp.key);  //created an adjlist node for the outincident vertex of temp
        while(out != NULL){ //check the outincident adjlist is not empty, go through all outincident vertices
            if(throwAway->dist[out->w] == INT_MAX){ //check the distance of outincident vertex is not update
                ItemPQ *new = malloc(sizeof(ItemPQ));   //allocate the memory for pqitem
                new->key = out->w;  //initialised the key of new to outincident vertex
                new->value = throwAway->dist[temp.key] + out->weight;   //set the value to the sum of temp's distance and outincident vertices' weight
                addPQ(q, *new); //add the new pqitem to pq
                addPred(throwAway,out->w,temp.key);     //add the key of temp to the pred list of outincident vertex
                throwAway->dist[out->w] = throwAway->dist[temp.key] + out->weight;  //update the distance of outincident vertex to the sum of temp's distance and outincident vertices' weight
            } else if(throwAway->dist[temp.key] + out-> weight == throwAway->dist[out->w]){ //check the sum of distance is equal to the distance of outincident vertex
                addPred(throwAway,out->w,temp.key); //add the key of temp to the pred list of outincident vertex
                ItemPQ *new = malloc(sizeof(ItemPQ));   //allocate the memory for pqitem
                new->key = out->w;  //initialised the key of new to outincident vertex
                new->value = throwAway->dist[temp.key] + out->weight;   //set the value to the sum of temp's distance and outincident vertices' weight
                addPQ(q, *new); //add the new pqitem to pq
            } else if(throwAway->dist[temp.key] + out->weight < throwAway->dist[out->w]){   //if find a shorter path
                PredNode *curr = throwAway->pred[out->w];   //created a curr prednode for outincident vertices' pred array
                while (curr->next != NULL) {    //go through every prednode
                    curr = curr->next;
                }
                curr->v = temp.key; //replaced the pred array for outincident vertex
                ItemPQ *new = malloc(sizeof(ItemPQ));   //allocate the memory for pqitem
                new->key = out->w;  //initialised the key of new to outincident vertex
                new->value = throwAway->dist[temp.key] + out->weight;   //set the value to the sum of temp's distance and outincident vertices' weight
                addPQ(q, *new); //add the new pqitem to pq
                throwAway->dist[out->w] = throwAway->dist[temp.key] + out->weight;  //update the distance of outincident vertex to the sum of temp's distance and outincident vertices' weight
            }
            out = out->next;
        }
    }
    int j;
    for(j = 0; j < throwAway->noNodes; j++){    //go through every node
        if(throwAway->dist[j] == INT_MAX){  //if node is unvisited
            throwAway->dist[j] = 0; //set the distance to 0
        }
    }

    return *throwAway;  //return the shortestpaths
}


//show the shortestpaths of all vertices
void showShortestPaths(ShortestPaths paths) {
    printf("%d\n",paths.src);   //print out the start point
    int i;
    for (i = 0; i<paths.noNodes; i++){  //go through all nodes
        printf(" i is %d:  ", i);   //indicate the vertex
        PredNode* tmp = paths.pred[i];
        while (tmp!= NULL){
            printf("->[%d] ", tmp->v);  //print out the paths
            tmp = tmp->next;
        }
        printf("\n");   //next line
    }

}

//free all the memory
void  freeShortestPaths(ShortestPaths paths) {
    int i;
    for (i=0; i< paths.noNodes; i++){   //go through every node
        PredNode* curr = paths.pred[i];
        while (curr!= NULL){
            PredNode* temp = curr;
            curr = curr->next;
            free(temp); //free the memory of pred array
        }
    }

}