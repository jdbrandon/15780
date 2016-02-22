'''
This file is where you put your solutions.
'''

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
    numItems = auction[0]
    if len(bid_list) == 0:
        return 0, auction[1][0], data

    maxBid = 0
    for bid in bid_list:
        if bid[1]:
            accountItems(items, auction[1][bid[0]])
        maxBid = bid[1]

    b = maxBid + 1
    overlap = False
    while b < (len(auction[1])):
        nextBid = auction[1][b]
        for item in nextBid[0]:
            if item in items:
                overlap = True
        if overlap:
            b = b + 1
            continue
        return b, auction[1][b], data


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
    A = [][]
    b = []
    if not bid_list:
        #construct LP
        for bid, p in auction[1]:
            c.append(p)

        for x in range(0, auction[0]):
            constraint = []
            for i, bid in enumerate(auction[1]):
                if x in bid[0]:
                    constraint.append(i)
            A.append(constraint)
        slackVars = len(A)
        for idx, constraint in enumerate(A):
            for i in range(0, slackVars):
                constraint.append(1 if idx == i else 0)
                b.append(1)
                I.append(slackVars+i)

        simplex.revized_simplex(I, c, A, b)

    for bid, p in auction[1]:
        sum_bids += p
    next_h = 0 if get_next_bid(auction, bid_list, data) is None else sum_bids
    return (next_h, data)


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
    pass


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
    pass

if __name__ == '__main__':
    a = (3, [([1,2], 2), ([2,3], 3), ([3], 2), ([1,3], 1)])
    print get_next_bid(a, [], [])
    print get_next_bid(a, [(0, True)], [])
    print get_next_bid(a, [(0, False)], [])
    print get_next_bid(a, [(0, False), (1, True)], [])
    print get_next_bid(a, [(0, False), (1, False)], [])

