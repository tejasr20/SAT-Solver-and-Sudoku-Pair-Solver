import sys
import os
from copy import deepcopy

fn="test5.cnf" #name of input file 
f=open(fn,"r")
line=f.readline()
while(line[0]=='c'):
    line=f.readline()
g=list(line.split(" "))
N=int(g[2]) #number of variables
M=int(g[4]) #number of clauses
l1=[i for i in range(1,N+1)]
cnf=[] #list of lists to store clauses in cnf form 
ls=[]

for i in range(1,M+1): #building up cnf
    line=f.readline()
    list0=list(line.split(" "))
    list1=[]
    list2=[]
    for j in list0:
        if(int(j)==0):
            break
        list1.append(int(j))
    cnf.append(list1)

def unit_propogate(cnf, l): #removes all clauses containing l and removes -l from all clauses containing -l,(l is assigned true)
    c=[]
    cl=[]
    for c in cnf:
        if(l in c):
            cl.append(c)
        if(-l in c):
            c.remove(-l)
    for x in cl:
        cnf.remove(x)

def DPLL(cnf, cnf_lit, literals):
    c=[]
    for c in cnf: #finding unit literals and doing unit propogation on them 
        if(len(c)==1):
            if(abs(c[0]) in cnf_lit):
                cnf_lit.remove(abs(c[0]))
            unit_propogate(cnf,c[0])
            literals.append(c[0])
            
    if(len(cnf)==0): #An empty formula implies that the original formula is SAT
        print("SAT")
        for i in range(1,N+1):
            if(i in literals):
                ls.append(i)
            elif(-i in literals):
                ls.append(-i)
            else:
                ls.append(i)
        print(ls)
        ls.clear()
        exit()
        return 1
    for c in cnf: #An empty clause in the formula implies that the original formula is UNSAT
        if(len(c)==0):
            return 0
    l=cnf_lit[0]
    return (DPLL(deepcopy(cnf)+[[l]],deepcopy(cnf_lit),deepcopy(literals)) | DPLL(deepcopy(cnf)+[[-l]],deepcopy(cnf_lit),deepcopy(literals)))


k=[]
(DPLL(cnf,l1,k))
print("UNSAT")


    
