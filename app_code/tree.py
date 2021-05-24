
print( "Loading tree.py" )

### Tree data structure

## each node takes the form:
## [parent_node, list_of_child_nodes, [action_path, state, cost, heuristic_value]]

def new_node():
         return [0, [], [[],[],0,0]]

def node_add_child( node, child ):
          node[1].append(child)
          child[0] = node
          return node

def node_set_children( node, children ):
          for child in children:
              node_add_child( node, child )
          return node

def node_get_children( node ):
          return node[1]

def node_set_parent( node, parent ):
       node[0] = parent
       parent[1].append(node)
       return node

def node_get_parent( node ):
       return node[0]


def node_set_path( node, path ):
       node[2][0] = path
       return node

def node_get_path( node ):
       return node[2][0]

def node_set_state( node, state ):
       node[2][1] = state
       return node

def node_get_state( node ):
       return node[2][1]

def node_set_cost( node, cost ):
       node[2][2] = cost
       return node

def node_get_cost( node ):
       return node[2][2]

def node_set_heuristic( node, heuristic ):
       node[2][3] = heuristic
       return node

def node_get_heuristic( node ):
       return node[2][3]


def node_get_path_length( node ):
       return len( node_get_path(node) )


def showlist( list ):
     for item in list:
         print( item )

def node_satisfies_goal( node, goal ):
        if goal in node_get_state(node):
           return True
        return False


def node_state_occurs_in_ancestor( node ):
      state = node_get_state(node)
      parent = node_get_parent(node)
      return node_state_occurs_in_upward_path( parent, state )


### Subordinate function for node_state_occurs_in_ancestor( node )
### now replaced by non-recursive version below
### Python blows up if you do very deep recursion (even tail recursion).

### Subordinate function for node_state_occurs_in_ancestor( node )
def node_state_occurs_in_upward_path( node, state ):
    while True:
      if node == 0:
         return False
      if node_get_state(node) == state:
         return True
      node = node_get_parent( node )


def node_get_depth( node ):
      depth = 0
      while True:
            if node == 0:
               return depth
            node = node_get_parent( node )
            depth = depth + 1




