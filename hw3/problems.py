'''
This file is where you put your solutions.
'''
import numpy as np
import copy as cp

'''
This function computes which next bid should be considered in the search, given the current search path.
You should consider the next bid with the lowest index that hasn't already been considered and does not overlap any bids already taken.
If there are no more bids to consider, this should return None (indicates that this is a goal state).

Input:
auction is a tuple (n, [...bids...]) as specified in the handout
bid_list is a list [(0, True), (4, False), ...] of tuples that indicate which bids were considered and whether they were taken or not (i.e. the current path of the search tree)
data is whatever you set for this node (as a result of auction_heuristic(...)) and can be used to cache information at every node of the search tree
For example, data can be used to keep track of which bids overlap with which other bids
You don't need to use data if you don't want to

Output:
A tuple (bid, data_taken, data_not_taken) or None
where bid is the index of the next bid to consider (the lowest index bid that hasn't already been considered and does not overlap any bids already taken)
data_taken is the new data for the node where this bid is taken
data_not_taken is the new data for the node where this bid is not taken
None is returned if there are no more bids to consider i.e. reached a goal
To be precise, a goal is reached when the bids that haven't yet been considered (the bids not in the current search path) all overlap with some bid that has been taken.

Notes:
The start node will be represented by bid_list = [] and data = None
The data_taken and data_not_taken will be passed to auction_heuristic(...) and can be used to help compute the hvalue.
There is a default implementation of auction_heuristic(...) initially given in this file, which looks the same as the one the autograder will use for this question.
We give this default implementation purely to show you how the autograder deals with data (it will just pass it along without changing it).
When testing, the autograder will be using its own version of auction_heuristic(...) so you are free to change your auction_heuristic(...) and it won't interfere with grading this question.
'''
def get_next_bid(auction, bid_list, data):
    items = []  
    if data:
        _,_,A,_,_,_ = data
        g1 = np.zeros(len(A[0]))
        g2 = np.zeros(len(A[0]))
    numItems = auction[0]
    if not bid_list:
        if data:
            g1[0] = -1
            g2[0] = 1
            return 0, cp.deepcopy(data + (g1,-1)), cp.deepcopy(data + (g2, 0))
        else:
            return 0, data, data

    maxBid = 0
    for bid in bid_list:
        if bid[1]:
            accountItems(items, auction[1][bid[0]])
        maxBid = bid[0]

    b = maxBid + 1
    while b < (len(auction[1])):
        overlap = False
        nextBid = auction[1][b]
        for item in nextBid[0]:
            if item in items:
                overlap = True
        if overlap:
            b = b + 1
            continue
        if data:
            g1[b] = -1
            g2[b] = 1
            return b, cp.deepcopy(data + (g1,-1)), cp.deepcopy(data + (g2, 0))
        else:
            return b, data, data
    return None


def accountItems(items, bid):
    for e in bid[0]:
        items.append(e)

'''
This function computes an admissible heuristic for the given node in the search tree.
Currently this just returns the simple admissible constant heuristic of taking all bids, or zero if the node is a goal.
Currently this just shows what the autograder will use to grade your get_next_bid(...).
You will modify this to compute the LP relaxation of the problem.
However you may want to keep a copy of this default version for your own testing purposes.
You need to properly cache the LP formulation and index set of the solution in data at the current node in order to hot-start the LP for the successor nodes.
To see exactly how the data parameter is passed around, see sample.py for the A* code.

Input:
auction is a tuple e.g. (n, [...bids...]) as specified in the handout
bid_list is a list e.g. [(0, True), (4, False), ...] of tuples that indicate which bids were considered and whether they were taken or not (i.e. the current path of the search tree)
data is whatever you set for this node in get_next_bid when computing the next bid and can be used to cache information at every node of the search tree
If bid_list is an empty list and parent_data is None, then this should give the heuristic for the start node

Output:
(hvalue, data)
An hvalue, representing an upper bound on the total price you can get with the remaining bids that haven't yet been considered
The final version of data that will be cached for this node (which will be passed into get_next_bid(...) when computing successors)
hvalue should be zero if this is a goal node

Notes:
The start node will be represented by bid_list = [] and data = None
The autograder will use your version of get_next_bid(...), so make sure to get that correct.
You should use one of your primal solvers for the start node, and your add_constraint(...) function for the other nodes.
You will probably have to modify your simplex solvers to return more information
'''
def auction_heuristic(auction, bid_list, data):
    sum_bids = 0
    I = []
    c = []
    A = []
    b = []
    if not bid_list:
        #construct LP
        for bid, p in auction[1]:
            c.append(-p)

        for x in range(0, auction[0]):
            constraint = []
            for i, bid in enumerate(auction[1]):
                if x in bid[0]:
                    constraint.append(1)
                else:
                    constraint.append(0)
            A.append(constraint)
        slackVars = len(A)
        slackStart = len(A[0])
        for idx, constraint in enumerate(A):
            for i in range(0, slackVars):
                constraint.append(1 if idx== i else 0)
            b.append(1)
        for i in range(0, slackVars):
            I.append(slackStart+i)
            c.append(0)

        val, soln, I = simplex_reference(np.array(I), np.array(c), np.array(A), np.array(b))
        newdata = (np.array(I),np.array(c),np.array(A),np.array(b),-val,soln)
    else:
        #complete DUAL LP using data
        I, c, A, b, val, soln, g, h = cp.deepcopy(data)
        branchBid = bid_list[len(bid_list)-1]

        nA, nb, nc, ret = add_constraint_reference(I, c, A, b, g, h)
        nval, nsoln, nI = ret
        nval = -nval
        for bid, taken in bid_list:
            if taken:
                nval -= auction[1][bid][1]

        newdata = (np.array(nI),np.array(nc),np.array(nA),np.array(nb),nval,nsoln)
    r = get_next_bid(auction, bid_list, newdata)
    if not r:
        if nval < 1e-14 and nval > -1e-14:
            return 0, newdata
        return nval, newdata
    next_h = newdata[4]
    return (next_h, newdata)


'''
This function computes one gomory cut given an LP solution.

Input:
A linear program with Ax = b and x >= 0
I is the index set.
A is a 2d numpy array
b is a 1d numpy array
m is such that the first m variables are basic variables, and the rest are slack variables

Output:
(coef, c)
where coef is a 1d numpy array of the coefficients for the basic variables such that np.dot(coef, x) >= c is the new constraint

When there is no fractional, basic variable, output None.


Notes:
The autograder will test this by comparing the outputted cut to the one from the reference solution.
This is independent of all the other questions. Assume all the linear programs have integer coefficients
in the constraints. Make sure not to modify the inputs.
'''
def gomory_cut(I, A, b, m):
    Ai = cp.deepcopy(A[:,I])
    AiInv = np.linalg.inv(Ai)

    minv = m
    mink = -1
    minxi = -1
    for k, i in enumerate(I):
        if i < m:
            xi = AiInv.dot(b)[k]
            f = xi - np.floor(xi)
            if (f >= 1e-12) and ((1-f) >= 1e-12):
                if minv > i:
                    minxi = xi
                    minv = i
                    mink = k
    if minv == m:
        return None
    k = mink
    fi = []
    c = minxi - np.floor(minxi)
    AiInvA = AiInv.dot(A)
    for j in range(0, len(A[0])):
        aij = AiInvA[k][j]
        delta = np.floor(aij)
        fij = aij-delta
        fi.append((fij, fij<=c))

    coef = c/(1-c)
    vec = []
    for f in fi:
        if f[1]:
            xi = f[0]
        else:
            xi = coef * (1 - f[0])
        vec.append(xi)
    return (np.array(vec), c)

'''
This function computes which next bid should be considered in the search, given the current searth path.
You should implement your own rule for picking which bid to branch on next.
To test this out, you will need to modify the code in sample.py to use this instead of get_next_bid(...)

Input:
auction is a tuple (n, [...bids...]) as specified in the handout
bid_list is a list [(0, True), (4, False), ...] of tuples that indicate which bids were considered and whether they were taken or not (i.e. the current path of the search tree)
data is whatever structure you set there for this node previously and can be used to cache information at every node of the search tree
You can use whatever you set for data to help pick the next bid

Output:
A tuple (bid, data_taken, data_not_taken) or None
where bid is the index of the next bid to consider
data_taken is the new data for the node where this bid is taken
data_not_taken is the new data for the node where this bid is not taken
None is returned if there are no more bids to consider i.e. reached a goal
To be precise, a goal is reached when the bids that haven't yet been considered (the bids not in the current search path) all overlap with some bid that has been taken.

Notes:
The start node will be represented by bid_list = [] and data = None
The autograder will be using your version of auction_heuristic(...), so make sure to get that correct.
'''
def get_next_bid_better(auction, bid_list, data):
    items = []  
    if data:
        _,_,A,_,_,_ = data
        g1 = np.zeros(len(A[0]))
        g2 = np.zeros(len(A[0]))
    numItems = auction[0]
    if not bid_list:
        if data:
            g1[0] = -1
            g2[0] = 1
            return 0, cp.deepcopy(data + (g1,-1)), cp.deepcopy(data + (g2, 0))
        else:
            return 0, data, data
    
    bidL = []
    for bid in bid_list:
        bidL.append(bid[0])
        if bid[1]:
            accountItems(items, auction[1][bid[0]])

    b = 0 
    validBids = []
    while b < (len(auction[1])):
        if b not in bidL:
            overlap = False
            nextBid = auction[1][b]
            for item in nextBid[0]:
                if item in items:
                    overlap = True
                    break
            if not overlap:
                validBids.append(b)
        b = b + 1
    maxv = None
    maxb = None
    validBids.reverse()
    for b in validBids:
        v = auction[1][b][1]
        if not maxv or v>maxv:
            maxv = v
            maxb = b

    if not maxb:
        return None
    else:
        if data:
            g1[maxb] = -1
            g2[maxb] = 1
            return maxb, cp.deepcopy(data + (g1,-1)), cp.deepcopy(data + (g2,0))
        else:
            return maxb, data, data

##########################################################
# INPUT description:
# Your algorithms receive 4 inputs:
# I <- an initial feasible basis
# c <- a numpy array that you will use as your objective function
# A,b <- a matrix and vector describing the constraint
#
#      A.dot(x) = b
#
# OUTPUT description:
# You algorithms should return two things:
# 1. the value of the optimal solution v.
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A restricted to index set I, called AI,
#       you can construct it with:
#
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
#
# return them with the statement: return (v, x)
##########################################################

##########################################################
# Implement any simplex algorithm here.
# You are free to write a dual and/or revised simplex
# implementation and call it here. It may be easier to
# write up the simpler standard simplex algorithm first,
# since you can reuse a lot of its code for the revised
# simplex algorithm anyway. It will also be useful as a
# reference.
##########################################################
def simplex(I, c, A, b):
    search = True
    while search:
        x = np.zeros(c.shape[0])
        AI = np.linalg.inv(A[:,I])
        cjbar = -1
        x[I] = AI.dot(b)
        k = -1
        for j in range(0,len(c)):
            if j not in I:
                t = c[j] - c[I].dot(AI.dot(A[:,j]))
                if t < 0:
                    cjbar = t
                    k = j
                    break
        if k == -1:
            return c[I].dot(x[I]), x
        dI = -AI.dot(A[:,k])
        xd = -x[I]/dI
        minV = None
        minI = -1
        j = 0
        for i in range(0,len(I)):
            if dI[i] < 0:
                if minV == None or xd[j] < minV:
                    minV = xd[j]
                    minI = j
            j = j + 1
        if minV == None:
            return -float("inf"), np.zeros(c.shape[0])
        I[minI] = k
    return False

##########################################################
# Implement a simplex algorithm with incremental
# A inverse computation here.
# You are free to write a dual simplex with incremental
# matrix inversion and call it here.
# In addition to output correctness, this algorithm
# will also be tested for speed. In our reference
# implementation, the speedup was a factor of 10-20
# for most instances.
##########################################################
def revised_simplex(I, c, A, b):
    search = True
    AI = np.linalg.inv(A[:,I])
    while search:
        x = np.zeros(c.shape[0])
        x[I] = AI.dot(b)
        k = -1
        cIAI = c[I].dot(AI)
        for j, v in enumerate(c):
            if j not in I:
                t = v - cIAI.dot(A[:,j])
                if t < 0:
                    k = j
                    break
        if k == -1:
            return c[I].dot(x[I]), x, I
        dI = -AI.dot(A[:,k])
        xd = -x[I]/dI
        minV = None
        minI = -1
        for i in range(len(I)):
            if dI[i] < 0:
                if minV == None or xd[i] < minV:
                    minV = xd[i]
                    minI = i
        if minV == None:
            return -float("inf"), np.zeros(c.shape[0]), I
        m = I[minI]
        I[minI] = k
        AI = updateAI(AI, A[:,k] - A[:,m], minI)
    return False, None, None

##########################################################
# Implement the dual simplex algorithm.
##########################################################
def dual_simplex(I, c, A, b):
    search = True
    AI = np.linalg.inv(A[:,I])
    AT = np.transpose(A)
    while search:
        x = np.zeros(c.shape[0])
        x[I] = AI.dot(b)
        minV = None
        for val in range(0, len(x)):
            if val in I:
                if x[val] <= 0:
                    if minV == None or x[val] < minV:
                        minV = x[val]
        k = -1
        for i in range(0,len(I)):
            if x[I[i]] == minV:
                k = i
                break
        if k == -1:
            return c[I].dot(x[I]), x
        #k is index of index in I
        v = AT.dot(np.transpose(AI)[:,k])
        minI = k

        cIAI = c[I].dot(AI)
        minV = None
        k = -1
        for j, f in enumerate(c):
            if j not in I:
                t = f - cIAI.dot(A[:,j])
                if v[j] < 0:
                    t = -(t/v[j])
                    if minV == None or t < minV:
                        minV = t
                        k = j

        if minV == None:
            return float("inf"), np.zeros(c.shape[0])

        m = I[minI]
        I[minI] = k
        AI = updateAI(AI, A[:,k] - A[:,m], minI)
    return False

def updateAI(AI, u, minI):
    return AI-np.outer(AI.dot(u), AI[minI])/(1+AI[minI].dot(u))

##########################################################
# Implement a method that add the new constraint g.T.dot(x) <= h
# to the existing system of equations
#
#    A.dot(x)=b.
#
# Then use dual simplex to solve this problem. You can assume
# that I is an index set which will yield a dual-feasible basis.
#
# OUTPUT description:
# You algorithms should return two things:
# 1. the value of the optimal solution v (for the new problem).
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x (for the new problem).
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A called AI, you can construct
#       it with:
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
#
# return them with the statement: return (v, x)
##########################################################
def add_constraint(I,c,A,b,g,h):
    v = []
    for i in range(0, len(A)):
        v.append([0])
    A = np.append(A, v, 1)
    g = np.append(g, [1], 0)
    A = np.append(A, [g], 0)
    b = np.append(b, h)
    I = np.append(I, len(A[0])-1)
    c = np.append(c, 0)
    x, y = dual_simplex(I,c,A,b)
    return x, y

# =============================================================================
# Below are the reference simplex solvers
# =============================================================================

##########################################################
# INPUT description:
# Your algorithm receives 4 inputs:
# I <- an initial feasible basis
# c <- a numpy array that you will use as your objective function
# A,b <- a matrix and vector describing the constraint
#
#      A.dot(x) = b
#
# OUTPUT description:
# You algorithms should return two things:
# 1. the value of the optimal solution v.
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A restricted to index set I, called AI,
#       you can construct it with:
#
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
# 3. the optimal index set
# return them with the statement: return (v, x, I)
##########################################################

##########################################################
# Implement any simplex algorithm here.
# You are free to write a dual and/or revised simplex
# implementation and call it here. It may be easier to
# write up the simpler standard simplex algorithm first,
# since you can reuse a lot of its code for the revised
# simplex algorithm anyway. It will also be useful as a
# reference.
##########################################################
def simplex_reference(I, c, A, b):
    while True:
        AI = np.linalg.inv(A[:,I])
        xI = AI.dot(b)
        cbar = c - A.T.dot(AI.T.dot(c[I]))
        j_neg = np.where(cbar < -1e-12)[0]
        if len(j_neg) == 0:
            x = np.zeros(c.shape[0])
            x[I] = xI
            return (c[I].dot(xI), x, I) # optimal, and return the index set
        dI = -AI.dot(A[:,j_neg[0]])
        if np.all(dI > 1e-12):
            return (-float("inf"), np.zeros(shape[0]))
        #print 'I,xI,dI,k'
        #print I
        #print xI, dI
        # find all entries that are zero-ish
        # treat them as very small negative steps i.e. alpha will be large
        dI[(dI >= -1e-12) & (dI <= 1e-12)] = -1e-12
        # xI should be all zero or positive, so randomly add some positive noise
        # so that argmin will randomly choose an index in case of ties
        k = np.argmin(-(xI + 1e-8*np.random.rand(xI.shape[0]))/dI + 1e10*(dI >= -1e-12))
        #print I[k], j_neg[0]
        I[k] = j_neg[0]


def basis_vector_reference(n, i):
    v = np.zeros(n)
    v[i] = 1.0
    return v

def sherman_morrison_reference(AI, index_out, col_in, col_out):
    basis_vec = basis_vector_reference(AI.shape[0], index_out)
    num_left = AI.dot(col_in) - AI.dot(col_out)
    num_right = basis_vec.T.dot(AI)
    #print "num_right", num_right
    num = np.outer(num_left, num_right)

    denom = 1 + basis_vec.T.dot(AI).dot(np.subtract(col_in, col_out))

    return AI - np.divide(num, denom)

##########################################################
# Implement a simplex algorithm with incremental
# A inverse computation here.
# You are free to write a dual simplex with incremental
# matrix inversion and call it here.
# In addition to output correctness, this algorithm
# will also be tested for speed. In our reference
# implementation, the speedup was a factor of 10-20
# for most instances.
##########################################################
def revised_simplex_reference(I, c, A, b):
    AI = np.linalg.inv(A[:,I])
    while True:
        #AI = np.linalg.inv(A[:,I])
        xI = AI.dot(b)
        cbar = c - A.T.dot(AI.T.dot(c[I]))
        j_neg = np.where(cbar < -1e-12)[0]
        if len(j_neg) == 0:
            x = np.zeros(c.shape[0])
            x[I] = xI
            return (c[I].dot(xI), x) # optimal
        dI = -AI.dot(A[:,j_neg[0]])
        if np.all(dI > 1e-12):
            return (-float("inf"), np.zeros(shape[0]))
        k = np.argmin(-xI/dI + 1e10*(dI > -1e-12))
        #print "In: ", j_neg[0], "Out: ", I[k]
        AI = sherman_morrison_reference(AI, k, A[:,j_neg[0]], A[:,I[k]])
        I[k] = j_neg[0]


##########################################################
# Implement the dual simplex algorithm.
# This algorithm requires additional output.
#
# OUTPUT description:
# You algorithms should return three things:
# 1. the value of the optimal solution v.
#     - Assuming an optimal solution x, get this with c.dot(x).
#     - Alternatively, you can use c[I].dot(xI), where xI
#       is the vector obtained from the optimal basis.
# 2. an optimal solution x
#     - This should be in the form of a numpy array.
#     - Assuming an optimal basis I and associated
#       inverse of A called AI, you can construct
#       it with:
#       x = np.zeros(c.shape[0])
#       x[I] = AI.dot(b)
# 3. the index set I for the optimal solution.
#
# return them with the statement: return (v, x, I)
##########################################################
def dual_simplex_reference(I, c, A, b):
    while True:
        #print 'I'
        #print I
        AI = np.linalg.inv(A[:,I])
        xI = AI.dot(b)
        cbar = c - A.T.dot(AI.T.dot(c[I]))
        i_neg = np.where(xI < -1e-12)[0]
        if len(i_neg) == 0:
            x = np.zeros(c.shape[0])
            x[I] = xI
            return (c[I].dot(xI), x, I) # optimal
        v = A.T.dot(AI.T[:,i_neg[0]])
        if np.all(v > 1e-12):
            return (-float("inf"), np.zeros(shape[0]))
        #print 'cbar, v'
        #print cbar,v
        # if v is positive, then we don't want to pick it
        # if v is zero, then we may want to pick it, so make it very small negative
        v[(v >= -1e-12) & (v <= 1e-12)] = -1e-12
        k = np.argmin(-(cbar+ 1e-8*np.random.rand(cbar.shape[0]))/(v) + 1e10*(v >= -1e-12))
        #print 'k, I[i_net[0]]'
        #print k, I[i_neg[0]]
        I[i_neg[0]] = k
# return the updated system as well as the solution
def add_constraint_reference(I,c,A,b,g,h):
    A = np.vstack([A, g])
    basis_vec = basis_vector_reference(b.shape[0]+1, b.shape[0])
    A = np.column_stack([A, basis_vec])
    b = np.append(b, h)
    I = np.append(I, [c.shape[0]])
    c = np.append(c, [0])
    return (A,b,c,dual_simplex_reference(I, c, A, b))
