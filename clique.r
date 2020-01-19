library(igraph)

create_graph <- function(k, n, p) {
  G <- make_full_graph(k)
  G <- add_vertices(G, n)
  
  for(i in V(G)) {
    for(j in V(G)) {
      deg <- degree(G)
      if (((i > k) && degree(G, i) < k-1) 
          || ((j > k) && degree(G, j) < k-1)) {
        if (runif(1) >= p){
          G <- add_edges(G, c(i,j))  
        }
      }
    }
  }
  # Keep the name of the nodes after deleting some
  V(G)$name <- V(G)
  return(G)
}

plot_graph <- function(G) {
  plot(G)
  Sys.sleep(2)
}

find_clique <- function(G) {
  active = TRUE
  marked_nodes = vector()
  
  while(active) {
    nodes = V(G)
    edges = E(G)
    degrees <- degree(G)
    
    # get the unmarked node with max cardinality
    candidate_nodes <- nodes[!nodes %in% marked_nodes]
    max_node <- candidate_nodes[which(degrees==max(degrees))][1]
    marked_nodes <- c(marked_nodes, max_node)
    
    print(paste('MAX NODE: ', max_node))
    print(paste('MARKED: ', marked_nodes))
    
    not_adjacent_nodes = c()
    for (node in nodes) {
      if (node != max_node && !are_adjacent(G, node, max_node)) {
        not_adjacent_nodes <- c(not_adjacent_nodes, node)
      }
    }
    V(G)$color <- ifelse(V(G) %in% not_adjacent_nodes , "red", "orange")
    plot_graph(G)
    
    if(length(not_adjacent_nodes) != 0) {
      print(not_adjacent_nodes)
      G <- delete_vertices(G, not_adjacent_nodes)
      print(G)
    } else {
      active <- FALSE
    }
    plot_graph(G)
  }
  return(G)
}


# k Cliquengröße
# n Zusätzliche Knoten, die nicht Teil der Clique sind
G <- create_graph(k=3, n=5, p=0.3)

# Verifikation:
print(clique_num(G)) # das sollte den gleichen Wert wie n ergeben
plot_graph(G)
clique <- find_clique(G)