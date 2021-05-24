#Problem
>Problem given by UoL 

The 8 queens problem asks for an arrangement of 8 queens on an 8 × 8 chess board so that no two queens can take each other. That is, no two of the queens can be in the same column, or in the same row,
or in the same 45 degree diagonal line.

This problem is given an m × n board, where m and n are any integers greater than zero, to find the smallest number of queens that
cover all the squares on the board. 

That is, to find the minimum number of queens which can be placed in such a way that every square on the board
either has a queen on it, or is in the same column, or in the same row, or in the
same 45 degree diagonal line (in any direction) as at least one queen. 

Unlike the 8 queens problem, there is no requirement about queens threatening each
other.

Solution uses queue_search.py and tree.py which were given by UoL.

#Usage
To use ensure all files are in the same directory
Use `qc_tester.py` to test application
It will be the format ` search( make_qc_problem(X,Y), ('A_star', zero_heuristic), Z, [])`
- Where X and Y are the board's dimensions
- And Z is the maximum search depth 