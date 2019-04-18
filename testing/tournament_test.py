from tournament import Bracket, Team
import sys
sys.path.insert(0, '../util')
from load_data import *
from scipy import mean

# Automatically picks the higher seed to win (region used as tiebreaker in final four)
def higher_seed_wins(t1,t2):
    return t1

# Automatically chooses the team with the lower id to win
def lower_id_wins(t1, t2):
    return t1 if t1.id < t2.id else t2

prediction_functions = {"Higher seed wins": higher_seed_wins, "Lower id wins": lower_id_wins}

#source: https://www.ncaa.com/news/basketball-men/bracket-beat/2017-01-10/march-madness-how-do-your-past-brackets-stack
average_scores = {2011: 53.12637, 2012: 82.98597, 2013: 69.97803, 2014: 60.14319, 2015: 83.25845, 2016: 68.17819, 2017: 65.66010}
mean = mean(list(map(lambda x: mean(average_scores[x]), average_scores)))

print("Average score for humans from 2011-2017: {}".format(mean))

for name, prediction_function in prediction_functions.items():
    #Need to specify path for calculation of team stats, results and glicko scores
    filename = '2dataMatrix.csv'

    s = []
    for year in range(2003,2018):
        filename = "{}dataMatrix.csv".format(year)
        b = Bracket(filename,year)
        if year in average_scores:
            s.append(b.score_tournament(prediction_function))
    print(name + " - Average Score: {}".format(sum(s)/len(s)))