import random
'''
This file is where you put your solutions.
'''


'''
This function computes the Q-learning update given a new (s,a,r,s') data point.

Input:
q is the current estimated Q-function that you should update in-place
alpha dictates how much of the new Q-value should mix with the current value
gammma is the discount factor
(s,a,r,ss) is the new data point
s was the current state
a was the action taken at s
r is the reward recieved
ss is the next state the MDP has transitioned to

Output:
No output is expected
q should be updated in-place
'''
def ql_update(q, alpha, gamma, s, a, r, ss):
    action = max(q[ss])
    q[s][a] = alpha * (r + gamma*action) + (1-alpha) * q[s][a]
    pass


'''
This function computes the greedy policy associated with the given Q-function

Input:
q is the current estimated Q-function

Output:
A policy which should be represented as a list (as explained in the handout)
The list will give an action for each state
'''
def ql_policy(q):
    p = []
    for state in q:
        v = max(state)
        i = state.index(v)
        p.append(i)
    return p

'''
This function performs one step of Q-learning
Given a new data point (s,a,r,ss), it will update the estimated Q-function in-place
Then it will determine the next action to take using an epsilon-greedy policy
You should use 0.3 for alpha and 0.1 for epsilon

Input:
q is the current estimated Q-function
gamma is the discount factor
(s,a,r,ss) is the new data point
s was the current state
a was the action taken at s
r is the reward recieved
ss is the next state the MDP has transitioned to

Output:
A tuple (greedy_a, a) where
greedy_a is the action that the greedy policy says to take for state ss
a is the action that the epsilon-greedy policy would take
You should also update the Q-function q in-place
'''
def ql_iteration(q, gamma, s, a, r, ss):
    ep = 0.1
    ql_update(q, 0.3, gamma, s, a, r, ss)
    greedy_a = q[ss].index(max(q[ss]))
    random.seed()
    r = random.random()
    a = greedy_a
    if r >= (1 - ep):
        a = int(random.random()*len(q[ss]))
    return (greedy_a, a)

'''
This function performs one step of Q-learning
Given a new data point (s,a,r,ss), it will update the estimated Q-function in-place
Then it will determine the next action to take using an epsilon-greedy policy
It is up to you how you want to set alpha and epsilon to try to learn more quickly

Input:
q is the current estimated Q-function
gamma is the discount factor
(s,a,r,ss) is the new data point
s was the current state
a was the action taken at s
r is the reward recieved
ss is the next state the MDP has transitioned to

Output:
A tuple (greedy_a, a) where
greedy_a is the action that the greedy policy says to take for state ss
a is the action that the epsilon-greedy policy would take
You should also update the Q-function q in-place
'''
def ql_iteration_tuned(i, q, gamma, s, a, r, ss):
    if i:
        ep = 1/(i*i)
    else:
        ep = 0.1
    ql_update(q, 0.3, gamma, s, a, r, ss)
    greedy_a = q[ss].index(max(q[ss]))
    random.seed()
    r = random.random()
    a = greedy_a
    if r >= (1 - ep):
        a = int(random.random()*len(q[ss]))
    return (greedy_a, a)
