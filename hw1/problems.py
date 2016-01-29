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
    ass = {}
    i = 0
    while i < n:
        if i not in ass:
            ass[i] = 0
        elif ass[i] == 0:
            ass[i] = 1
        count = count + 1
        if check(formula, ass):
            if len(ass) == n:
                return ass, count
        else:
            if ass[i] == 0:
                continue
            elif ass[i] == 1:
                while i >= 0 and ass[i] == 1:
                    del ass[i]
                    i = i - 1
                if i == -1:
                    return False, count
                continue
        i = i + 1
    return False, count

################################################################################
# Simple Sat Problem Solver with unit propagation
## Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments were tried
################################################################################
def unitSolver(n, formula):
    count = 0
    bval = []
    ass = {}
    i = 0
    if not propSingles(formula, ass):
        return False, count
    valid = True
    tmp = myCopy(formula)
    while i < n:
        if i not in ass:
            ass[i] = 0
            bval.append(i)
        elif ass[i] == 0 and not valid:
            ass[i] = 1
        else:
            i = i + 1
            continue
        count = count + 1
        valid = True
        if check(formula, ass):
            if len(ass) == n:
                return ass, count
            if propVal(i, ass[i], formula):
                if propSingles(formula, ass):
                    if check(formula, ass):
                        if len(ass) == n:
                            return ass, count
                        i = i + 1
                        continue #skip backtrack
        #Case: backtracking
        dellist = []
        for v in ass:
            if v not in bval:
                if v != i:
                    dellist.append(v)
        for v in dellist:
            del ass[v]
        valid = False
        formula = myCopy(tmp)
        if ass[i] == 0:
            continue #try the 1 branch of this variable
        elif ass[i] == 1:
            #backtrack to previous branch val
            while ass[i] == 1 and len(bval) > 0:
                i = bval.pop()
            if len(bval) == 0:
                return False, count
    return False, count

#Returns false if assignment fails
def propSingles(formula, ass, recent = -1):
    recurse = True
    while recurse:
        recurse = False
        for clause in formula:
            if len(clause) == 1:
                var = clause[0][1]
                if var not in ass:
                    ass[var] = 0 if clause[0][0] else 1
                    recent = var
                    print "prop", ass
                    if not check(formula, ass):
                        return False, recent
                    ret = propVal(var, ass[var], formula)
                    if not ret:
                        return False, recent
                    if ret == -1:
                        recurse = True
                elif bool(ass[var]) == bool(clause[0][0]):
                    #a singleton for which the current assigment
                    #will always produce a false clause
                    return False
    print "r",recent
    return True, recent

#Returns false when a contradiction occurs
def propVal(var, val, f):
    ret = True
    for clause in f:
        for literal in clause:
            if literal[1] == var:
                tval = bool(val) != bool(literal[0])
                if tval:
                    for l2 in clause:
                        if l2 != literal:
                            clause.remove(l2)
                    break
                else:
                    clause.remove(literal)
                    if len(clause) == 1:
                        #special case, need to recurse
                        #another call to propSingles
                        ret = -1
                    if len(clause) == 0:
                        return False
    return ret

def myCopy(f):
    ret = []
    for clause in f:
        tmp = []
        for literal in clause:
            tmp.append((literal[0],literal[1]))
        ret.append(tmp)
    return ret

################################################################################
# Clause Learning SAT Problem Solver                      
# Input: n is the number of variables (numbered 0, ..., n-1).
#        formula is CNF
# Output: An assignment that satisfies the formula
#         A count of how many variable assignments where tried
#         A list of all conflict-induced clauses that were found
################################################################################
def clauseLearningSolver(n, formula):
    count = 0
    bval = []
    ass = {}
    ig = None
    learned = []
    recent = -1
    level = 0
    i = 0
    if not propSingles(formula, ass):
        return False, count, learned
    valid = True
    tmp = myCopy(formula)
    while i < n:
        if i not in ass:
            ass[i] = 0
            print "0",ass
            bval.append(i)
            ig = Node(level, i, ass[i], [])
            print "implies", ig.implies
        elif ass[i] == 0 and not valid:
            ass[i] = 1
            print "1",ass
        else:
            i = i + 1
            continue
        recent = i
        count = count + 1
        valid = True
        if check(formula, ass):
            if len(ass) == n:
                return ass, count, learned
            if propVal(i, ass[i], formula):
                ret, recent = propSingles(formula, ass, recent)
                print "r",recent
                if ret:
                    if check(formula, ass):
                        if len(ass) == n:
                            return ass, count, learned
                        i = i + 1
                        continue #skip backtrack
        #Case: backtracking
        print "learn", ass
        learned.append(createLearnedClause(ass, bval, recent))
        recent = -1
        dellist = []
        for v in ass:
            if v not in bval:
                if v != i:
                    dellist.append(v)
        for v in dellist:
            del ass[v]
        print "del",ass
        valid = False
        formula = myCopy(tmp)
        if ass[i] == 0:
            continue #try the 1 branch of this variable
        elif ass[i] == 1:
            #backtrack to previous branch val
            while ass[i] == 1 and len(bval) > 0:
                i = bval.pop()
            recent = i
            if len(bval) == 0:
                return False, count, learned
    return False, count, learned

def createLearnedClause(a,b,r):
    print a,b,r
    clause = []
    for v in a:
        if v in b or v == r:
            continue
        clause.append((a[v],v)) #value of variable becomes negation bit... woah
    return clause

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
    g = [[(0,0), (1, 1)],[(0,1), (0,2)],[(0,1), (1,2)]]
    m = [[(0,0)],[(1,0)]]
    #checkCheck(f)
    #simple(f, 5)
    #simple(h, 3)
    #simple(g, 3)
    #unit(f,5)
    #unit(h,3)
    #unit(g,3)
    #unit(m,1)
    claus(g,3)

def claus(f, n):
    print clauseLearningSolver(n, f)

def unit(f, n):
    print unitSolver(n, f)

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

class Node:
    level = 0
    var = 0
    val = 0
    impliedBy = []
    implies = []
    def __init__(self, level, var, val, implied):
        self.level = level
        self.var = var
        self.val = val
        self.impliedBy.extend(implied)

if __name__ == "__main__":
    main()
