from __future__ import print_function

print( "Loading queue_search.py" )
from random import *   # used for randomised depth first search
from tree import   *   # defines tree data structure
import time            # used to determine runtime
import sys             # used to flush the output buffer

## The main interface function is:
##     search(PROBLEM, STRATEGY, MAX_NODES, OPTIONS )
##
## PROBLEM is a problem specification tuple of the form:
##     ( initialise_func,     # function for problem initialisation (if not required put None)
##       problem_info_func,   # function to print out basic info about the problem
##       initial_state,       # initial state for search 
##       poss_act_func,       # function operating on a state to return list of possible actions
##       successor_func,      # function operating on an action and a state to return successor state
##       goal_test_func       # Boolean function operating on a state to test if it is a goal
##     )
##
## Typically the PROBLEM argument will be a function call that returns a problem tuple.
##
## STRATEGY can be one of the following:
## 'breadth_first'
## 'depth_first'
## 'randomised_depth_first'
## ('uniform_cost', cost_func )
## ('best_first', heuristic_func )  
## ('A_star', heuristic_func, cost_func )
## ('A_star', heuristic_func)              ## if cost_func is omitted it defaults to path length
##
## heuristic_func  is a function that operates on a state to return an estimate of distance to goal
## cost_func       is a function that operates on a **node** to give the cost of reaching that node
##
## MAX_NODES is the maximum number of nodes that will be explored
##
## OPTIONS is a list, which can contain any selection of the following:
## 'node_dots'   --- print a dot every time a node is expanded (just so you can tell it is running)
## 'loop_check'  --- check if node already generated and if so discard it
## 'print_loops' --- print indication when a loop is detected (only useful with 'loop_check')
## 'print_ties' --- print indication when a new node ties in cost/heurstic with an existing node.

 
global OPTIONS

def search(problem, strategy, max_nodes, options ):

    print( "======= Running Brandon's Python Queue-Based Search Procedure =======" )

    initialise_func    = problem[0]
    problem_info_func  = problem[1]
    initial_state      = problem[2]
    poss_act_func      = problem[3]
    successor_func     = problem[4]
    goal_test_func     = problem[5]
    global OPTIONS     
    OPTIONS            = options

    if not(initialise_func == None):
       ## apply( initialise_func, () ) # Call function to initialise problem
       initialise_func()  # Call function to initialise problem
       
    ##apply( problem_info_func, () )  # Call function to print problem info
    problem_info_func()  # Call function to print problem info
    
    print( "Strategy:", strategy )
    print( "Search Limit: max_nodes =", max_nodes )
    print( "Options:", options )
    print( "*** starting search ***" )

    start_time = time.process_time()

    node_queue = get_initial_node_queue( initial_state )
    for nodes_tested in range(max_nodes):
          ##print_node_queue(node_queue)
          if 'node_dots' in options:
             print_function( ".", end = '' )
          if nodes_tested % 1000 == 0:
             print( nodes_tested, ' ', end = '' )
             sys.stdout.flush() ## flush output to force immediate printing
          if node_queue == []:
             print( "\n:-( <FAILURE> )-:" )
             print( "The entire search space was searched --- this problem has NO SOLUTION!" )
             print( "Total nodes tested = " + str(nodes_tested+1) )
             print( "Time taken =", time.process_time() - start_time, "seconds\n" )
             return False
          first_node = node_queue.pop(0)  #take 1st node from queue
          if 'loop_check' in options and node_state_occurs_in_ancestor( first_node ):
             if 'print_loops' in options:
                print( "loop detected", end = '' )
             continue
          if 'show_expand' in options:
             print( "Expanding ", end = '' )
             print( node_get_state( first_node ) )
              
          #if apply(goal_test_func, [node_get_state( first_node )] ):
          if goal_test_func( node_get_state( first_node ) ):   
             action_path = node_get_path(first_node)
             print( "\n:-)) *SUCCESS* ((-:" )
             print( "The action path to the solution is:" )
             print_action_list(action_path)
             print( "Path length = " + str( len(action_path) ) )
             print( "Total nodes tested = " + str(nodes_tested+1) )
             print( "Time taken =", time.process_time() - start_time, "seconds\n" )
             return action_path
          children = node_get_children(node_expand( first_node, 
                                                    poss_act_func,
                                                    successor_func 
                                                  )
                                      )
          node_queue = add_to_node_queue(strategy, node_queue, children)
    print( "\n:-( <FAILURE> )-:" )
    print( "Search aborted --- node limit reached (MAX_NODES=%i)\n" % max_nodes )
    print( "Time taken =", time.process_time() - start_time, "seconds\n" )
    return False

def get_initial_node_queue( initial_state ):
    return [node_set_state( new_node(), initial_state )]


def node_expand(node, poss_actions, successor_fun ):

      state = node_get_state( node )
      path  = node_get_path( node )
      suc_pairs = possible_action_successor_pairs(state, poss_actions, 
                                                         successor_fun)
      for suc_pair in suc_pairs:
          action = suc_pair[0]
          result_state = suc_pair[1]
          child = new_node()
          node_set_parent( child, node )
          node_set_path( child, path + [action] )
          node_set_state( child, result_state ) 
      return node           


def possible_action_successor_pairs(state, poss_actions, successor_fun ):
       ##poss_acts = apply( poss_actions, [state] )
       poss_acts = poss_actions( state )
       ##return [(action, apply(successor_fun, (action,state))) for action in poss_acts]
       return [(action, successor_fun(action,state)) for action in poss_acts]

    
def add_to_node_queue( strategy, node_queue, new_nodes ):
        if (strategy == 'breadth_first'):
           return node_queue + new_nodes
        if (strategy == 'depth_first'):
           return new_nodes + node_queue
        if (strategy == 'randomised_depth_first'):
           shuffle(new_nodes)
           return new_nodes + node_queue
        if (strategy[0] == 'best_first'):
           heuristic_func = strategy[1]
           return add_nodes_according_to_heuristic(new_nodes, node_queue, heuristic_func )
        if (strategy[0] == 'uniform_cost'):
           cost_func = strategy[1]
           return add_nodes_according_to_cost(new_nodes, node_queue, cost_func )
        if (strategy[0] == 'A_star'):
           heuristic_func = strategy[1]
           ## cost_func = node_get_path_length  ## default cost function for A_star search
           cost_func = node_get_depth  ## default cost function for A_star search

           if len(strategy) == 3: 
              cost_func = strategy[2]
           return add_nodes_according_to_A_star(new_nodes, node_queue, 
                                                cost_func, heuristic_func )
        print( "ERROR: unknown strategy: " + strategy )


######### Heuristic and cost based functions for adding to the queue ###############

### Need to update and modularise this part of the code
### Really it needs just one "weight" value stored on each node
### The add_nodes function should be passed the weight function.

def add_nodes_according_to_heuristic(new_nodes, node_queue, heuristic_func ):
         for new_node in new_nodes:
            ##new_h = apply( heuristic_func, [node_get_state(new_node)])
            new_h = heuristic_func( node_get_state(new_node) )
            
            node_set_heuristic( new_node, new_h ) ## also store heuristic of new node
            inserted = False
            for i in range(len(node_queue)):
                qih = node_get_heuristic(node_queue[i])
                if (new_h <= qih):
                   if ((new_h == qih) and 'print_ties' in OPTIONS):
                      print( "TIE: nodes tie on heuristic", 
                              node_get_state(new_node), 
                              node_get_state(node_queue[i]) )
                   node_queue.insert(i, new_node)
                   inserted = True
                   break
            if not(inserted):
               node_queue.append(new_node)
         return node_queue         


def add_nodes_according_to_cost(new_nodes, node_queue, cost_func ):
         for new_node in new_nodes:
            ## new_c = apply( cost_func, [new_node])
            new_c = cost_func( new_node )
            node_set_cost( new_node, new_c ) ## also store cost of new node
            inserted = False
            for i in range(len(node_queue)):
                qic = node_get_cost(node_queue[i])
                if (new_c <= qic):
                   if ((new_c == qic) and 'print_ties' in OPTIONS):
                      print( "TIE: nodes tie on cost", 
                              node_get_state(new_node), 
                              node_get_state(node_queue[i]) )
                   node_queue.insert(i, new_node)
                   inserted = True

                   break
            if not(inserted):
               node_queue.append(new_node)
         return node_queue   

def add_nodes_according_to_A_star(new_nodes, node_queue, cost_func, heuristic_func ):
         for new_node in new_nodes:
            ##new_h = apply( heuristic_func, [node_get_state(new_node)])
            new_h = heuristic_func(node_get_state(new_node))
            ##new_c = apply( cost_func, [new_node])
            new_c = cost_func(new_node)
            node_set_heuristic( new_node, new_h ) 
            node_set_cost( new_node, new_c )

            new_Astar = new_h + new_c ## Astar ranking based on heuristic + cost

            inserted = False
            for i in range(len(node_queue)):
                qi_Astar = node_get_cost(node_queue[i]) + node_get_heuristic(node_queue[i])
                if (new_Astar <= qi_Astar):
                   if ((new_Astar == qi_Astar) and 'print_ties' in OPTIONS):
                      print( "TIE: nodes tie on Astar value", 
                              node_get_state(new_node), 
                              node_get_state(node_queue[i]) )
                   node_queue.insert(i, new_node)
                   inserted = True
                   break
            if not(inserted):
               node_queue.append(new_node)
         return node_queue        


#### A few handy functions ####

def print_node_queue(node_queue):
     print( "node_queue" )
     for n in node_queue:
         print( node_get_state(n) )

                                
def print_action_list( act_list ):
     print( ", ".join([action_string(action) for action in act_list]) )

#def action_string( action ):
#          return " ".join(action)

def action_string( action ):
          return str(action)





