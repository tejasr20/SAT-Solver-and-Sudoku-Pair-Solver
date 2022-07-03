# CS202-I Assignment 1
## Sudoku Pair Solver and Pair Generator 

The zip file contains 2 source code files, test cases, and the explanation document.
The source code and test files are named as follows:
1)sudoku_pair_solver.py for the first part 
2)sudoku_pair_generator.py for the second part 
3)Test folder contains 5 solvable and 2 unsatisafiable test case files with their solutions. Three files are solvable 9x9 Sudokus and two are 16x16 sudokus. They are named as follows:
    (i)test1_9x9.csv, test1_9x9_solved.csv
    (ii)test2_9x9.csv, test2_9x9_solved.csv
    (iii)test3_9x9.csv, test3_9x9_solved.csv
    (iv)test1_16x16.csv, test1_16x16_solved.csv
    (v)test2_16x16.csv, test2_16x16_solved.csv
    (vi) test_UNSAT_9x9.csv
    (vii) test_UNSAT_16x16.csv
    
The first source code takes sudoku dimension k as input from the terminal ("Enter k: " will be displayed) and the tester will also have to enter the name of the input csv file which is in the same directory as the test code( This will be prompted by the message " Enter the name of the input csv file which must be the same directory:"). 
On running the code for q1, the output will be 2N lines of N numbers each, of which the first N lines represents the first sudoku and the subsequent N lines represents the second sudoku in the pair. The solved sudoku pair output which will be displayed will satisfy all standard sudoku constraints as well as the constraint that corresponding cells in the sudoku pair do not have the same values. Additionally, the solved sudoku pair will also be stored in a csv file called "out_solved.csv" in the same directory.


The second source code takes sudoku dimension k as input from the terminal ("Enter k: " will be displayed) which the user has to enter. The output, or generated maximal sudoku pair will be created in a file 'out.csv' in the same directory as the source code. The code will also print the two generated output sudokus along with creating the out.csv file.  
'Out.csv' will be a csv file containing 2N lines of N numbers, of which the first N lines represents the first sudoku and the subsequent N lines represents the second sudoku in the pair. This will satisfy all standard sudoku constraints as well as the constraint that corresponding cells in the sudoku pair do not have the same values. Additionally, it will be a maximal sudoku pair for the solved version of the same pair.

