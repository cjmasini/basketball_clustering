import os
import pandas as pd
import numpy as np
from constants import *

def create_matrix(year_num):
    df = pd.read_csv(KAGGLE_RAW_PATH+"TeamSpellings.csv", encoding = "ISO-8859-1")
    ids = pd.Series(df.TeamID.values,index=df.TeamNameSpelling).to_dict()
    kenpom_matrix = pd.DataFrame(columns=['year','team_id','adj_tempo','adj_off_eff','adj_def_eff','adj_eff', 'seed'])
    year=str(year_num)[-2:]
    kenpom = pd.read_csv(KENPOM_RAW_PATH+'summary{}_pt.csv'.format(year))
    for team in kenpom['TeamName']:
        if team == team:
            row = kenpom.loc[kenpom['TeamName'] == team]
            kenpom_matrix = kenpom_matrix.append({"year": int(year_num), "team_id": int(ids[team]), "adj_tempo": row.seed.values[0], 'adj_off_eff':row.AdjOE.values[0],'adj_def_eff':row.AdjDE.values[0],'adj_eff':row.AdjEM.values[0],'seed':row.seed.values[0]},ignore_index=True)

    kenpom_matrix.year = kenpom_matrix.year.astype(int)
    kenpom_matrix.team_id = kenpom_matrix.team_id.astype(int)
    kenpom_matrix.to_csv(KENPOM_PROCESSED_PATH+'{}kenpom_processed.csv'.format(year_num))
    print("Created matrix {}kenpom_processed.csv".format(year_num))
    return kenpom_matrix

if __name__ == "__main__":
    for i in range(2003,2018):
        create_matrix(i)
    