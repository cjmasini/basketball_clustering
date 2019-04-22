import pandas as pd
import numpy as np
import os
from sklearn import preprocessing


def load_data():
    data = pd.DataFrame()
    for year in range(2003,2018):
        filename = "../data/data_matrices/tournament_stats/{}tournamentStats.csv".format(year)
        df = pd.read_csv(filename)
        df = df.rename(columns={ df.columns[0]: "team_id" })
        df.set_index('team_id',inplace=True)
        df=df.transpose()
        df['year'] = year
        data = data.append(df)
    return data

def load_normalized_data():
    data = pd.DataFrame()
    for year in range(2003,2018):
        filename = "../data/data_matrices/tournament_stats/{}tournamentStats.csv".format(year)
        df = pd.read_csv(filename)
        df = df.rename(columns={ df.columns[0]: "team_id" })
        df.set_index('team_id',inplace=True)
        df=df.transpose()
        df = normalize(df)
        df['year'] = year
        data = data.append(df)
    return data

def load_normalized_data_without_year(year):
    data = load_normalized_data()
    return data.loc[data["year"] != year]

def load_normalized_year_data(year):
    data = load_normalized_data()
    return data.loc[data["year"] == year]

def load_team_data(team_id, year):
    data = load_data()
    data = data.loc[data["year"]==year]
    return data.loc[str(team_id)]

def load_normalized_team_data(team_id, year):
    data = load_normalized_data()
    data = data.loc[data["year"]==year]
    return data.loc[str(team_id)]

def normalize(df):
    for col in df.columns:
        df[col] = (df[col] - df[col].mean())/df[col].std(ddof=0)
    return df

def get_wins(team_id, year, path_to_combined = "../data/data_matrices/tournament_matrices/dataMatrix_combined.csv"):
    df = pd.read_csv(path_to_combined)
    tournament = df[np.logical_and(df['tourny'] == 1, df['year'] == year)]
    num_games = len(tournament)
    tournament = tournament.iloc[num_games-63:num_games]
    tournament = tournament[np.logical_or(tournament['id_0'] == team_id, tournament['id_1'] == team_id)]
    return len(tournament)-1

#print(load_normalized_data())