# Queen cover problem
# Problem given by UoL


from __future__ import print_function
from copy import deepcopy

#Sets board to matrix of 0
def queen_get_initial_state(x,y):
      return ( 0, 0, matrix_of_zeros(y,x) )

#defines a matrix of size X by Y of zeros's
def matrix_of_zeros(X,Y):
    return [ [0 for x in range(X)] for y in range(Y)]

#gets locations that the queen can go
def queen_possible_locations( state ):
    if state[0] == 0:
        return queen_initial_locations()
    return queen_following_locations(state)

#creates intial locations for the queen
def queen_initial_locations():
           moves = []
           #loop through the board
           for i in range(BOARD_X):
               for j in range(BOARD_Y):
                   moves = moves + [[i,j]]
           return moves

def queen_following_locations( state ):
    moves = []
    for i in range(BOARD_X):
        for j in range(BOARD_Y):
            if state[2][i][j] == 0  or state[2][i][j]  == 3:
                moves = moves + [[i,j]]
    return moves

#the board which is created when the queen moves
def queen_initial_successor( action ):
  board = deepcopy(queen_initial_state[2])
  board = update(board, action[0], action[1])
  return( 1, action, board )

def queen_successor_state( action, state ):
    if state[0] == 0:
       newstate =  queen_initial_successor( action )
       return newstate

    board = deepcopy(state[2])
    numOfQueens = state[0] + 1

    board = update(board, action[0], action[1])
    return (numOfQueens, (action[0],action[1]), board)

#update the baord
def update(board, x, y):
    for yLoop in range(BOARD_Y):
        #Horizontal (left to right)
        if board[x][yLoop] !=1:
            board[x][yLoop]= 2

    for xLoop in range(BOARD_X):
        # vertical (top to bottom)
        if board[xLoop][y] !=1:
            board[xLoop][y]= 2

    ##Create the diagonal One for: top left, top right, bottom left, bottom right
    a=x
    b=y
    while b<BOARD_Y and a>=0:
        if board[a][b] !=1:
            board[a][b] = 3
        a=a-1
        b=b+1
    a=x
    b=y
    while b<BOARD_Y and a<BOARD_X:
        if board[a][b] !=1:
            board[a][b] = 3
        a=a+1
        b=b+1

    a=x
    b=y
    while b>=0 and a<BOARD_X:
        if board[a][b] !=1:
            board[a][b] = 3
        a=a+1
        b=b-1
    a=x
    b=y
    while b>=0 and a>=0:
        if board[a][b] !=1:
            board[a][b] = 3
        a=a-1
        b=b-1

    board[x][y] = 1

    return board

#shows what the board looks like in the Goal state
def queen_goal_state( state ):
    board = state[2]
    #Goal state is board with no 0's
    for xLoop in range(BOARD_X):
        for yLoop in range(BOARD_Y):
            if board[xLoop][yLoop] == 0:
                return False

    print( "\nGOAL STATE:" )
    print_board_state( state )

    return True

#prints the current chess board representation
def print_board_state( state ):
    #Displays board
      board = state[2]
      for row in board:
           for square in row:
               print( " %2i" % square, end = '' )
           print()



def queen_print_problem_info():#Prints information about the problem
    print( "The Queen's Cover Problem (Board of:",BOARD_X,"x",BOARD_Y,")" )

## Return a problem spec tuple for a given board size
def make_qc_problem(x, y):
      global BOARD_X, BOARD_Y, queen_initial_state
      BOARD_X = x
      BOARD_Y = y
      queen_initial_state = queen_get_initial_state(x,y)
      return  ( None,
                queen_print_problem_info,
                queen_initial_state,
                queen_possible_locations,
                queen_successor_state,
                queen_goal_state
              )
