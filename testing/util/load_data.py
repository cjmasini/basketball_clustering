import pandas as pd
import numpy as np
import os
from sklearn import preprocessing


def load_data():
    data = {}
    for year in range(2003,2017):
        filename = "../data/data_matrices/tournament_stats/{}tournamentStats.csv".format(year)
        df = pd.read_csv(filename)
        df = df.rename(columns={ df.columns[0]: "team_id" })
        df.set_index('team_id',inplace=True)
        df=df.transpose()
        data[year] = df
    return data

def load_normalized_data():
    data = {}
    for year in range(2003,2017):
        filename = "../data/data_matrices/tournament_stats/{}tournamentStats.csv".format(year)
        df = pd.read_csv(filename)
        df = df.rename(columns={ df.columns[0]: "team_id" })
        df.set_index('team_id',inplace=True)
        df=df.transpose()
        data[year] = normalize(df)
    return data

def load_normalized_data_as_dataframe():
    data = None
    for year in range(2003,2017):
        filename = "../data/data_matrices/tournament_stats/{}tournamentStats.csv".format(year)
        df = pd.read_csv(filename)
        df = df.rename(columns={ df.columns[0]: "team_id" })
        df.set_index('team_id',inplace=True)
        df=df.transpose()
        if data is None:
            data = normalize(df)
            continue
        data = data.append(normalize(df))
    return data

def load_normalized_year_as_dataframe(year):
    filename = "../data/data_matrices/tournament_stats/{}tournamentStats.csv".format(year)
    df = pd.read_csv(filename)
    df = df.rename(columns={ df.columns[0]: "team_id" })
    df.set_index('team_id',inplace=True)
    df=df.transpose()
    return normalize(df)

def load_team_data(team_id, year):
    data = load_data()[year]
    return data.loc[str(team_id)]

def load_normalized_team_data(team_id, year):
    data = load_normalized_data()[year]
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
