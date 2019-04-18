import pandas as pd
import numpy as np
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

