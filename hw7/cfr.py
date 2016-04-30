import sys
import numpy as np
from game import Game


regret = {}

# game will be an instance of Game, which is defined in game.py
# num_iterations is the number of CFR iterations you should perform.
# An iteration of CFR is one traversal of the entire game tree.
def solve_game(game, num_iterations):
    #############################
    # The goal of your algorithm is to fill
    # strategy_profile with equilibrium strategies.
    # strategy_profile[p][i][a] should return
    # the probability of player p choosing the particular
    # action a at information set i in the equilibrium
    # you compute.
    #
    # An example set of values for a small game with 2
    # information sets for each player would be:
    #    strategy_profile[0][0] = [0.375, 0.625]
    #    strategy_profile[0][1] = [1,0]
    #
    #    strategy_profile[1][0] = [0.508929, 0.491071]
    #    strategy_profile[1][1] = [0.666667, 0.333333]
    strategy_profile = {0:{}, 1:{}}
    for node in range(game.num_nodes):
        tmp = {}
        tmpr = {}
        if not game.is_leaf(node):
            if game.get_current_player(node) == -1:
                continue
            n = game.get_num_actions_node(node)
            for i in range(n):
                tmpr[i] = 0
                tmp[i] = 1/float(n)
            p = game.get_current_player(node)
            infoSet = game.get_node_infoset(node)
            if infoSet not in strategy_profile[p]:
                strategy_profile[p][infoSet] = tmp
            if infoSet not in regret:
                regret[(p,infoSet)] = tmpr

    #######################
    # Implement CFR in here
    #######################
    for i in range(num_iterations):
       cfr(game, game.get_root(), [1, 1], strategy_profile)
       strategy_profile
    normalize(strategy_profile)
    return strategy_profile

def cfr(game, node, reach, sp):
    if game.is_leaf(node):
        u = game.get_leaf_utility(node)
        return np.array([u * reach[1], -u * reach[0]])
    player = game.get_current_player(node)
    ev = np.zeros(2)
    actions = game.node_action_names[node]
    if(player  == -1):
        for i, a in enumerate(actions):
            new_reach = []
            new_reach.append(reach[0] * game.get_nature_probability(node,i))
            new_reach.append(reach[1] * game.get_nature_probability(node,i))
            ev += cfr(game, game.get_child_id(node, i), new_reach, sp)
    else:
        infoset = game.get_node_infoset(node)
        action_ev = {}
        opponent = 1-player
        infoSet = game.get_node_infoset(node)
        prob = getStrategy((player,infoSet), len(actions))
        for i,_ in enumerate(actions):
            new_reach = [0,0]
            p = prob[i]
            sp[player][infoSet][i] += reach[player] * p
            new_reach[player] = reach[player] * p
            new_reach[opponent] = reach[opponent]
            action_ev[i] = cfr(game, game.get_child_id(node, i), new_reach, sp)
            ev[player] += p * action_ev[i][player]
            ev[opponent] += action_ev[i][opponent]
        for i, _ in enumerate(actions):
            regret[(player,infoset)][i] += (action_ev[i][player]-ev[player])
    return ev

def getStrategy(node, num_actions):
    strat = {}
    s = 0
    for i in range(num_actions):
        strat[i] = regret[node][i] if regret[node][i] > 0 else 0
        s += strat[i]
    for i in range(num_actions):
        if s > 0:
            strat[i] /= float(s)
        else:
            strat[i] = 1/float(num_actions)
    return strat

def normalize(sp):
    for p in sp:
        for k in sp[p]:
            s = sum(sp[p][k].values())
            for a in sp[p][k]:
                sp[p][k][a] /= s

if __name__ == "__main__":
    # feel free to add any test code you want in here. It will not interfere with our testing of your code.
    # currently, this file can be invoked with:
    # python cfr.py <path/to/gamefile> <num CFR iterations>

    filename = sys.argv[1]
    iterations = int(sys.argv[2])

    game = Game()
    game.read_game_file(filename)

    strategy_profile = solve_game(game, iterations)

    print game.compute_strategy_profile_ev(strategy_profile)
