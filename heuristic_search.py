from tournament import *
from game_agent import CustomPlayer, moves_combined

import sys
from datetime import datetime

def play_round_2(agents, num_matches):
    """
    Play one round (i.e., a single match between each pair of opponents)
    """
    agent_1 = agents[-1]
    wins = 0.
    total = 0.
    
    for idx, agent_2 in enumerate(agents[:-1]):

        counts = {agent_1.player: 0., agent_2.player: 0.}
        names = [agent_1.name, agent_2.name]

        # Each player takes a turn going first
        for p1, p2 in itertools.permutations((agent_1.player, agent_2.player)):
            for _ in range(num_matches):
                score_1, score_2 = play_match(p1, p2)
                counts[p1] += score_1
                counts[p2] += score_2
                total += score_1 + score_2

        wins += counts[agent_1.player]

    return 100. * wins / total

def main(filename=None):
    MATCHES = 20
    HEURISTICS = [("Null", null_score),
                  ("Open", open_move_score),
                  ("Improved", improved_score)]
    MM_ARGS = {"search_depth": 3, "method": 'minimax', "iterative": False}
    AB_ARGS = {"search_depth": 5, "method": 'alphabeta', "iterative": False}
    CUSTOM_ARGS = {"method": 'alphabeta', 'iterative': True}
    
    mm_agents = [Agent(CustomPlayer(score_fn=h, **MM_ARGS),
                       "MM_" + name) for name, h in HEURISTICS]    
    ab_agents = [Agent(CustomPlayer(score_fn=h, **AB_ARGS),
                       "AB_" + name) for name, h in HEURISTICS]
    random_agents = [Agent(RandomPlayer(), "Random")]
    alphas = [x * 0.01 for x in range(0, 120, 20)]
    test_agents = [Agent(CustomPlayer(score_fn=moves_combined(a), **CUSTOM_ARGS),
                         "Alpha"+str(a))
                   for a in alphas]
    results = []
    print(datetime.now())
    for agentUT in test_agents:
        print(agentUT.name)
        #agents = mm_agents + random_agents + ab_agents + [agentUT]
        agents = ab_agents + [agentUT]
        results.append(play_round_2(agents, MATCHES))
    print(datetime.now())
    if filename: # save the result into a text
        with open(filename, 'w') as f:
            lines = [str(alphas[i])+'\t'+str(results[i])
                     for i in range(len(alphas))]
            for line in lines:
                print(line, file=f)
    
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        main(filename)
    except IndexError:
        main()
