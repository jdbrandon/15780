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
        #TODO: make strategy based on infoset rather than node
        if not game.is_leaf(node):
            n = game.get_num_actions_node(node)
            regret[node] = {}
            for i in range(n):
                regret[node][i] = 0
                tmp[i] = 1/float(n)
            p = game.get_current_player(node)
            strategy_profile[p][node] = tmp

    #######################
    # Implement CFR in here
    #######################
    for i in range(num_iterations):
        cfr(game, game.get_root(), [1, 1], strategy_profile)
    print strategy_profile
    return strategy_profile

def cfr(game, node, reach, sp):
    #game.print_node_info(node)
    if game.is_leaf(node):
        u = game.get_leaf_utility(node)
        return np.array([u * reach[0], -u * reach[1]])
    player = game.get_current_player(node)
    infoset = game.get_node_infoset(node)

    ev = np.zeros(2)
    actions = game.node_action_names[node]
    if(player  == -1):
        for i, a in enumerate(actions):
            new_reach = []
            new_reach.append(reach[0] * game.get_nature_probability(node,a)) #may need to use i instead of a
            new_reach.append(reach[1] * game.get_nature_probability(node,a))
            ev += cfr(game, game.get_child_id(node, i), new_reach, sp)
    else:
        action_ev = {}
        opponent = 1-player
        for i, a in enumerate(actions):
            new_reach = [0,0]
            p = sp[player][node][i]
            sp[player][node][i] += reach[player] * p
            new_reach[player] = reach[player] * p
            new_reach[opponent] = reach[opponent]
            action_ev[a] = cfr(game, game.get_child_id(node, i), new_reach, sp)
            ev[player] += p * action_ev[a][player]
            ev[opponent] += action_ev[a][opponent]
        for a in actions:
            regret[node][i] += (action_ev[a][player]-ev[player])
    return normalize(ev)

def normalize(ev):
    print "start", ev
    ev[0] = 0 if ev[0] < 0 else ev[0]
    ev[1] = 0 if ev[1] < 0 else ev[1]
    s = ev[0]+ev[1]
    ev = [ev[0]/s,ev[1]/s]
    ev[0] = 0 if ev[0] < 0.0001 else ev[0]
    ev[1] = 0 if ev[1] < 0.0001 else ev[1]
    print "normal", ev
    return ev




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
