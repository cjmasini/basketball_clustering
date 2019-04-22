from tournament import Bracket, Team
import sys
sys.path.insert(0, './util')
from load_data import *

# Automatically picks the higher seed to win (region used as tiebreaker in final four)
def higher_seed_wins(t1,t2):
    return t1

# Automatically chooses the team with the lower id to win
def lower_id_wins(t1, t2):
    return t1 if t1.id < t2.id else t2

def more_similar_wins(t1, t2):
    # use k means to create clusters here
    wins1 = 0
    for team in cluster1:
        wins1 += get_wins(team[0])
    wins2 = 0
    for team in cluster1:
        wins2 += get_wins(team[0])


prediction_functions = {"Higher seed wins": higher_seed_wins, "Lower id wins": lower_id_wins}

for name, prediction_function in prediction_functions.items():
    s = []
    for year in range(2003,2018):
        filename = "{}dataMatrix.csv".format(year)
        b = Bracket(filename,year)
        s.append(b.score_tournament(prediction_function))
    print(name + " - Average Score: {:0.2f}".format(sum(s)/len(s)))