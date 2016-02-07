import numpy as np

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
    print I, c, A, b
    search = True
    while search:
        AI = np.linalg.inv(A[:,I])
        minV = 0
        cjbar = -1
        for j in range(0,len(c)):
            if j not in I:
                txi = AI.dot(b)
                print "xi",txi
                t = c[j] - c[I].dot(AI[:,j])
                print t
                if t < minV:
                    xI = txi
                    minV = t
                    cjbar = j
        if cjbar == -1:
            x = np.zeros(c.shape[0])
            x[I] = AI.dot(b)
            return c[I].dot(xI), x
        print minV, cjbar
        dI = -(AI.dot(A[:,cjbar]))
        print dI
        xd = -xI/dI
        minV = xd[0]
        minI = 0
        for i in range(1, len(xd)):
            if xd[i] < minV:
                minV = xd[i]
                minI = i

        I[minI] = cjbar
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
    return False

##########################################################
# Implement the dual simplex algorithm.
##########################################################
def dual_simplex(I, c, A, b):
    return False

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
    return False


simplex(np.array([2,3]),
np.array([-2,-1,0,0]),np.array([np.array([1,2,1,0]),np.array([3,1,0,1])]), np.array([6,9]))
