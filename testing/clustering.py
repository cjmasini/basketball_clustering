from sklearn.cluster import KMeans, SpectralClustering
import numpy as np
import util.load_data as ld

def kmeans(team_id, year = 2017, n_clusters = 91):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data_without_year.values)
    prediction = kmeans.predict([team.values[:-1]])
    cluster = []
    for i, c in enumerate(kmeans.labels_):
        if c == prediction:
            cluster.append(i)
    teams = []
    for index in cluster:
        teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
    return teams

#print(kmeans(1291)) #1243, 1374, 1291,1344 are other ids
