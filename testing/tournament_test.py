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

prediction_functions = {"Higher seed wins": higher_seed_wins, "Lower id wins": lower_id_wins}

for name, prediction_function in prediction_functions.items():
    #Need to specify path for calculation of team stats, results and glicko scores
    filename = '2dataMatrix.csv'

    s = []
    for year in range(2003,2018):
        filename = "{}dataMatrix.csv".format(year)
        b = Bracket(filename,year)
        s.append(b.score_tournament(prediction_function))
    print(name + " - Average Score: {:0.2f}".format(sum(s)/len(s)))