from tournament import Bracket, Team
import sys
sys.path.insert(0, './util')
from load_data import *
from clustering import kmeans

# Automatically picks the higher seed to win (region used as tiebreaker in final four)
def higher_seed_wins(t1, t2, year=2017):
    return t1

# Automatically chooses the team with the lower id to win
def lower_id_wins(t1, t2, year=2017):
    return t1 if t1.id < t2.id else t2

def k_means_predictor(t1, t2, year=2017):
    cluster1 = kmeans(t1.id, year)
    cluster2 = kmeans(t2.id, year)
    wins1 = []
    for team in cluster1:
        wins1.append(get_wins(team[0], year))
    wins2 = []
    for team in cluster1:
        wins2.append(get_wins(team[0], year))
    return t1 if 1.*sum(wins1)/len(wins1) >= 1.*sum(wins2)/len(wins2) else t2


prediction_functions = {"Higher seed wins": higher_seed_wins, "Lower id wins": lower_id_wins, 'k-means': k_means_predictor}

for name, prediction_function in prediction_functions.items():
    s = []
    for predict_year in range(2003,2018):
        for year in [i for i in range(2003,2018) if i != predict_year]:
            filename = "{}dataMatrix.csv".format(year)
            b = Bracket(filename,year)
            s.append(b.score_tournament(prediction_function,year))
    print(name + " - Average Score: {:0.2f}".format(sum(s)/len(s)))