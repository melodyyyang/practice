// Graph ADT interface for Ass2 (COMP2521)
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "Graph.h"

typedef struct GraphRep{
	AdjList *edges; //array of lists
	int nV; //number of vertices
	int nE; //number of edges
}GraphRep;

static AdjList newnode(int v, int weight);

//create a new graph
Graph newGraph(int noNodes) {
    
    assert(noNodes >= 0);   //check number of nodes can't be negative
    
    int i;
    Graph new = malloc(sizeof(GraphRep));   //allocate memory for a new graph 
    new->nV = noNodes;  //initialized nV to noNodes
    new->nE = 0;    //initialized nE to 0
    
    new->edges = malloc(sizeof(AdjList)*noNodes);   //allocate memory for array of lists
    for (i = 0; i < noNodes; i++)
        new->edges[i] = NULL;   //set the array edges to NULL
    return new;
}
        
        
//create a new AdjListNode     
static AdjList newnode(int v, int weight){

	AdjList new = malloc(sizeof(adjListNode));  //allocate memory for new AdjListNode
	new->w = v;
	new->weight = weight;
	new->next = NULL;   //set the next of the node to NULL
	return new;
}
    
   
//insert a given edge(from src to dest) in to graph
void  insertEdge(Graph g, Vertex src, Vertex dest, int weight) {
	assert(g != NULL);  //check graph can't be NULL
	
	AdjList new = newnode(dest, weight);    //create a new AdjListNode for dest
	
	new->next = g->edges[src];  
    g->edges[src] = new;    //insert new edge in the front of edges[src]
	g->nE++;    //increase the number of edges
}

//remove a given edge(from src to dest) from graph
void  removeEdge(Graph g, Vertex src, Vertex dest) {
	assert(g != NULL);  //check graph can't be NULL

	AdjList curr = g->edges[src];   //create an AdjListNode for all edges of src
	
	if(curr->w == dest){    //if dest is an edge of src
		g->edges[src] = curr->next; //delete the edge(src to dest)
		g->nE--;    //decrease the number of edges
		return;
	}
	while(curr->next->w != dest){    //go through all edges of src
		curr = curr->next;
	}
	AdjList temp = curr->next;
	curr->next = curr->next->next;	//removed the edge
	free(temp);	//free the memory of the deleted edge
	g->nE--;    //decrease the number of edges
}


//check if there is an edge between src and dest
bool adjacent(Graph g, Vertex src, Vertex dest) {
	assert(g != NULL);  //check graph can't be NULL

	AdjList curr = g->edges[src];   //create an AdjListNode for all edges of src
	while(curr != NULL){    //go through all edges of src
		if(curr->w == dest){
			return true;    //find an edge between src and dest
		}else{
			curr = curr->next;  //check every node untill find the edge
		}
	}
	return false;   //no edge between src and dest
}

//number of verticies in the graph
int numVerticies(Graph g) {
	assert(g != NULL);

	return g->nV;
}

//all edges of v
AdjList outIncident(Graph g, Vertex v) {
	assert(g != NULL);

	return g->edges[v];
}


//all incoming edges from v
AdjList inIncident(Graph g, Vertex v) {
	assert(g != NULL);	//check graph can't be NULL

	AdjList new = newnode(-1, -1);	//create an invalid adjlist node
	AdjList temp = new;	//create another invalid adjlist node
	int i;
	for(i = 0; i < g->nV; i++){	//go through the edges of all verticies
		AdjList curr = g->edges[i];	//create a current adjlist node
		while(curr != NULL){	//go through every node
			if(curr->w == v){	//check there is an edge between i and v
				if(temp->w == -1){
					temp->w = i;
					temp->weight = curr->weight;
				}
				AdjList node = newnode(i, curr->weight);
				AdjList next = temp->next;
				node->next = next;
				temp->next = node;	//return temp at right position
			}
			curr = curr->next;
		}
	}
	if(temp->w == -1){	//if there is no inincidentnode
		return NULL;
	}
	return temp;
}

//print out graph g
void  showGraph(Graph g) {
	assert(g != NULL);

    int i;
    for(i = 0; i < g->nV; i++){
        AdjList curr = g->edges[i];
        printf("%d", i); //print out the start points
        while(curr != NULL){
        	printf("->");
            printf("%d", curr->w);  //print out the end points
            printf(" weight:%d", curr->weight); //print out the weight between start and end point
            curr = curr->next;  //go through all vertices
        }
        printf("\n");
    }
}


//free the memory of graph
void  freeGraph(Graph g) {
	assert(g != NULL);

    int i;
    for(i = 0; i < g->nV; i++){
        AdjList curr = g->edges[i];
        while(curr != NULL){
            AdjList temp = curr;    //let temp equal to the edges
            curr = curr->next;  //go through all vertices
            free(temp); //free the memory of AdjList
        }
    }
    free(g);    //free the memory of graph
}
