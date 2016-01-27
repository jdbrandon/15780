################################################################################
# Check if a given partial assignment is consistent with the cnf
# Input: formula is a CNF encoded as described in the problem set.
#        ass is a dictionary of assignments.
# Output: Whether there is a clause that is false in the formula.
################################################################################
def check(formula, ass):
    for clause in formula: #of the form (x0 or ~x1 or x3)
        ret = 0
        for v in clause:
            if(v[1] in ass):
                ret = ret or (ass[v[1]] if v[0] == 0 else not ass[v[1]])
            else:
                ret = 1 #special case, cant determine if clause is false yet
                break
        if(not ret): 
            return False #if a clause in the formula is false, return false
    return True #all clauses evaluate to true

################################################################################
# Simple Sat Problem Solver
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments were tried
################################################################################
def simpleSolver(n, formula):
    count = 0
    jump = False
    ass = {}
    i = 0
    while i < n:
        if(jump):
            ret, count = simpleHelp(formula, ass, i, 1, count)
            jump = False
        else:
            ret, count = simpleHelp(formula, ass, i, 0, count)
        if ret:
            if len(ass) == n:
                return ass, count
            i = i + 1
            continue
        else:
            ret, count = simpleHelp(formula, ass, i, 1, count)
            if ret:
                if len(ass) == n:
                    return ass, count
                i = i + 1
                continue
            else:
                #both 0 and 1 produce failure
                #jumpback
                maxV = -1
                clause = getClause(formula, ass)
                for v in clause:
                    if v[1] > maxV and ass[v[1]] != 1:
                        maxV = v[1]
                if maxV == -1:
                    return False, count
                #prune ass
                j = i
                while j > maxV:
                    del ass[j]
                    j = j-1
                i = maxV
                jump = True
                #TODO: learn something?
                continue
        i = i + 1
    return False, count

def getClause(f,a):
    for clause in f:
        ret = 0;
        for v in clause:
            if(v[1] in a):
                ret = ret or (a[v[1]] if v[0] == 0 else not a[v[1]])
            else:
                ret = 1
                break
        if(not ret):
            return clause
    print "error!!!"
    return []

def simpleHelp(f, ass, i, v, c):
    ass[i] = v
    c = c + 1
    return check(f, ass), c

################################################################################
# Simple Sat Problem Solver with unit propagation
## Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments were tried
################################################################################
def unitSolver(n, formula):
    return False, 0

################################################################################
# Clause Learning SAT Problem Solver                      
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments where tried
#         A list of all conflict-induced clauses that were found
################################################################################
def clauseLearningSolver(n, formula):
    return False, 0, []

################################################################################
# Conflict-directed backjumping with clause learning SAT Problem Solver                      
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments where tried
################################################################################
def backjumpSolver(n, formula):
    return False, 0, []

def main():
    f = [[(1,0),(0,2),(0,3)],[(0,1),(1,4)],[(0,0), (0,1), (0,2), (0,3), (0,4)]]
    h = [[(1,0)],[(0,1),(0,2)],[(0,1),(1,2)],[(1,1),(0,2)],[(1,1),(1,2)]]
    #checkCheck(f)
    simple(f, 5)
    simple(h, 3)

def simple(f, n):
    print simpleSolver(n, f)

def checkCheck(f):
    a = {1:1, 3:0, 4:1}
    b = {0:1, 1:0, 2:0, 3:0, 4:0}
    c = {0:0, 1:0, 2:0, 3:0, 4:1}
    print check(f,a)
    print check(f,b)
    print check(f,c)
    print check(f, {4:1});
    print check(f, {4:1, 1:0});

if __name__ == "__main__":
    main()
