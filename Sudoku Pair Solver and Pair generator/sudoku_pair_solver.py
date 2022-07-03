from pysat.solvers import Solver
from pysat.card import *
import os
import csv
import sys
import pandas as pd
import time 

start=time.time()
g=Solver()
cnf=CNF()
clues=[]
K=int(input("Enter k:"))
N=K*K
string=str(input("Enter the name of the input csv file which must be the same directory:"))
start=time.time()
with open(string, newline='') as f:
    reader = csv.reader(f)
    count=0
    for row in reader:
        data = list(row)
        map_object = map(int, data)
        list_of_integers = list(map_object)
        clues.append(list_of_integers)

    # encoding that the cell at (r,c) has the value v
    def var(r, c, v): # The fucntion var gives mpas variables of the form x_{rcv} to a natural number.
        assert(1 <= r and r <= 2*N and 1 <= c and c <= N and 1 <= v and v <= N)
        return (r-1)*N*N+(c-1)*N+(v-1)+1

    # Build the clauses for the first sudoku in cnf
    for r in range(1,N+1): # r runs over 1,...,N
        for c in range(1, N+1): # each cell holds exactly one value 
            cnf.extend(CardEnc.equals(lits=[var(r,c,v) for v in range(1,N+1)],encoding=EncType.pairwise))
    for v in range(1, N+1):
        # Each row has the value v exactly once
        for r in range(1, N+1): 
            cnf.extend(CardEnc.equals(lits=[var(r,c,v) for c in range(1,N+1)],encoding=EncType.pairwise))
        # Each column has the value v exactly once
        for c in range(1, N+1): 
            cnf.extend(CardEnc.equals(lits=[var(r,c,v) for r in range(1,N+1)],encoding=EncType.pairwise))
        # Each subgrid has the value v exactly once
        for sr in range(0,K): 
            for sc in range(0,K): 
                cnf.extend(CardEnc.equals(lits=[var(sr*K+rd,sc*K+cd,v) for rd in range(1,K+1) for cd in range(1,K+1)],encoding=EncType.pairwise))
        
    #building clauses for second sudoku in pair 
    for r in range(N+1,2*N+1): # r runs over N,...,2*N
        for c in range(1, N+1):
            cnf.extend(CardEnc.equals(lits=[var(r,c,v) for v in range(1,N+1)],encoding=EncType.pairwise))
    for v in range(1, N+1):
        # Each row has the value v
        for r in range(N+1, 2*N+1): 
            cnf.extend(CardEnc.equals(lits=[var(r,c,v) for c in range(1,N+1)],encoding=EncType.pairwise))
        # Each column has the value v
        for c in range(1, N+1): 
            cnf.extend(CardEnc.equals(lits=[var(r,c,v) for r in range(N+1,2*N+1)],encoding=EncType.pairwise))
        # Each subgrid has the value v
        for sr in range(K,2*K):
            for sc in range(0,K):
                cnf.extend(CardEnc.equals(lits=[var(sr*K+rd,sc*K+cd,v) for rd in range(1,K+1) for cd in range(1,K+1)],encoding=EncType.pairwise))  
        
    # adding atomic propositions to cnf according to the clues given 
    for r in range(1, 2*N+1):
        for c in range(1, N+1):
            if(clues[r-1][c-1]!=0):
                cnf.extend(CardEnc.equals(lits=[var(r,c,clues[r-1][c-1])],encoding=EncType.pairwise))

    # This adds clauses to cnf such that no corresponding cell in the sudoku pair holds the same value
    for r in range(1,N+1):
        for c in range(1,N+1):
            for v in range(1,N+1):
                cnf.extend(CardEnc.atmost(lits=[var(r,c,v),var(r+N,c,v)],encoding=EncType.pairwise))

g.append_formula(cnf.clauses, no_return=False)
f=g.solve()
if(f==False):
        print(None) # No solution exists for the given sudoku pair 
else:
    s=(g.get_model())
    pos=[]
    for i in s: # concatanates all the positive/true variables into the list pos. 
        if(i>0):
            pos.append(i)  
    # pos allows us to extract the solved sudoku pair by taking an "inverse" of var.
    sol=[] #used to print the solved sudoku pair 
    count=0
    arr=[]
    for i in range(1,2*N+1):   
        arr.append([0]*N)
    print("This is the first solved sudoku:")
    for i in pos:
        r=(i-1)//(N*N)
        c=((i-1)%(N*N)//N)
        v=(((i-1)%(N*N)%N)+1)
        sol.append(v)
        arr[r][c]=v
        if (len(sol)==N):
            print(sol)
            count+=1
            sol.clear()
        if(count==N):
            print("This is the second solved sudoku:")
            count=0
    end=time.time()
    print("Time is ",end-start)
    outname = 'out_solved.csv' 
    df=pd.DataFrame(arr)
    df.to_csv(outname,index=False, header=False)