from pysat.solvers import Solver
from pysat.card import *
import random
import os
import csv
import pandas as pd
import time 

start=time.time()
g=Solver()
cnf=CNF()
clues=[]
K=int(input("Enter k:"))
N=K*K
start=time.time()

# We first obtain a solved sudoku pair from two empty sudoku's using the appropriate clauses
# After that, we remove values from the solved sudoku pair appropriateley until we get a maximal pair.

# encoding that the cell at (r,c) has the value v
def var(r, c, v): # The fucntion var gives mpas variables of the form x_{rcv} to a natural number.
    assert(1 <= r and r <= 2*N and 1 <= c and c <= N and 1 <= v and v <= N)
    return (r-1)*N*N+(c-1)*N+(v-1)+1

# Build the clauses for the first sudoku in cnf
for r in range(1,N+1): # r runs over 1,...,N
    for c in range(1, N+1): # each cell holds exactly one value 
        cnf.extend(CardEnc.equals(lits=[var(r,c,v) for v in range(1,N+1)],encoding=EncType.pairwise))
for v in range(1, N+1):
    # # Each row has the value v exactly once
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

# This adds the sudoku pair constraint that no corresponding cell holds the same value.
for r in range(1,N+1):
    for c in range(1,N+1):
        for v in range(1,N+1):
            cnf.extend(CardEnc.atmost(lits=[var(r,c,v),var(r+N,c,v)],encoding=EncType.pairwise))

# pos gives us all the filled places at any point of time in the sudoku pair 
# Remove() is a recursive function. In each iteration, it removes as many elements as possible from pos,
# such that the sudoku pair still has a unique solution. In the final iteration of Remove(), the length 
# of pos remains the same, because no more elements can be removed from the sudoku pair without violating
# uniqueness of solution. Hence, Remove() will return pos such that the sudoku pair is maximal.
def Remove(pos, l):
    for i in pos:
        index=pos.index(i)
        k=pos.pop(index)
        g1=Solver()
        for j in pos:
            g1.add_clause([j])
        g1.append_formula(cnf.clauses, no_return=False)
        count=0
        # print(g1.solve())
        for m in g1.enum_models():
            count+=1
        # print(count)
        if(count>1):
            pos.append(i)
        g1.delete()
    l1=len(pos)
    if(l1==l):
        return pos
    else:
        return Remove(pos,l1)

cnf.extend(CardEnc.equals(lits=[var(random.randint(1,N),random.randint(1,N),random.randint(1,N))],encoding=EncType.pairwise))
g.append_formula(cnf.clauses)
g.solve()
t=(g.get_model())
pos=[]
x=[]
temp=[]
for i in t:
    if(i>0):
        pos.append(i)
        x.append(-i)

l=(len(pos))
random.shuffle(pos)
temp=Remove(pos,l) 
temp.sort()
sol=[]
for i in range(1,2*N+1):   
    sol.append([0]*N)

for i in temp:
    r=(i-1)//(N*N)
    c=((i-1)%(N*N)//N)
    v=(((i-1)%(N*N)%N)+1)
    sol[r][c]=v
count=0
print("This is the first generated sudoku: \n" )
for y in sol:
    count+=1
    print(y)
    if(count==N):
        print("This is the second generated sudoku:\n")

outname ='out.csv' # The generated sudoku pair will be created in file 'out.csv' in the same directory   
df=pd.DataFrame(sol)
df.to_csv(outname,index=False, header=False)
end=time.time()
print("The time of execution of above program is :", end-start)



