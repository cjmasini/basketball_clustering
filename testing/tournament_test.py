from tournament import Bracket, Team
import sys
sys.path.insert(0, './util')
from util.load_data import *
from clustering import *

# Automatically picks the higher seed to win (region used as tiebreaker in final four)
def higher_seed_wins(t1, t2, year=2017):
    return t1

# Automatically chooses the team with the lower id to win
def lower_id_wins(t1, t2, year=2017):
    return t1 if t1.id < t2.id else t2


def clustering_predictor(t1, t2, year=2017, func=None):
    if func is not None:
        cluster1 = func(t1.id, year)
        cluster2 = func(t2.id, year)
        wins1 = []
        for team in cluster1:
            wins1.append(get_wins(team[0], team[1]))
        wins2 = []
        for team in cluster2:
            wins2.append(get_wins(team[0], team[1]))
        try:
            return t1 if 1.*sum(wins1)/len(wins1) >= 1.*sum(wins2)/len(wins2) else t2
        except:
            return t1
    else:
        print("ERROR: func not defined in predictor")

def k_means_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, kmeans)

def spectral_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, spectral)

def hierarchical_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, hierarchical)

def birch_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, birch)

def pca_kmeans_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, pca_kmeans)

def kneighbors_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, kneighbors)

def pca_kneighbors_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, pca_kneighbors)

def pca_hierarchical_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, pca_hierarchical)

def pca_spectral_predictor(t1, t2, year=2017):
    return clustering_predictor(t1, t2, year, pca_spectral)

prediction_functions = {"spectral": spectral_predictor, 'k-means': k_means_predictor, "pca_k-means": pca_kmeans_predictor,
"pca_kneighbors": pca_kneighbors_predictor, "pca_hierarchical": pca_hierarchical_predictor, "pca_spectral": pca_spectral_predictor}

for name, prediction_function in prediction_functions.items():
    s = []
    year = 2017
    for year in range(2003,2018):
        filename = "{}dataMatrix.csv".format(year)
        b = Bracket(filename,year)
        s.append(b.score_tournament(prediction_function,year))
        print(name + " - Average Score: {:0.2f}".format(sum(s)/len(s)))