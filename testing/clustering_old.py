from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering, Birch
from sklearn.decomposition import PCA
import numpy as np
import util.load_data as ld

def clustering(team_id, year = 2017, n_clusters = 91, func=None, fittable=None):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    if func is not None and fittable is not None:
        data = ld.load_normalized_data_without_year(year)
        data["team_id_copy"] = data.index
        data_without_year = data.drop("year", axis=1)
        data_without_year = data_without_year.drop("team_id_copy", axis=1)
        latest = ld.load_normalized_year_data(year)
        team = ld.load_normalized_team_data(team_id, year)
        if fittable:
            model = func(n_clusters=n_clusters).fit(data_without_year.values)
            prediction = model.predict([team.values[:-1]])
            cluster = []
            for i, c in enumerate(model.labels_):
                if c == prediction:
                    cluster.append(i)
        else:
            labels = func(n_clusters=n_clusters).fit_predict(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
            prediction = labels[-1]
            labels = labels[:-1]
            cluster = []
            for i, c in enumerate(labels):
                if c == prediction:
                    cluster.append(i)
        teams = []
        for index in cluster:
            teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
        return teams
    else:
        print("ERROR: Either func or fittable is None!")

def kmeans(team_id, year = 2017, n_clusters = 91):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=0).fit(data_without_year.values)
    prediction = kmeans_model.predict([team.values[:-1]])
    cluster = []
    for i, c in enumerate(kmeans_model.labels_):
        if c == prediction:
            cluster.append(i)
    teams = []
    for index in cluster:
        teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
    return teams

def spectral(team_id, year = 2017, n_clusters = 160):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    labels = SpectralClustering(n_clusters=n_clusters, random_state=0).fit_predict(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
    prediction = labels[-1]
    labels = labels[:-1]
    cluster = []
    for i, c in enumerate(labels):
        if c == prediction:
            cluster.append(i)
    teams = []
    for index in cluster:
        teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
    return teams

def hierarchical(team_id, year = 2017, n_clusters = 160, linkage="ward"):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    labels = AgglomerativeClustering(n_clusters=n_clusters).fit_predict(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
    prediction = labels[-1]
    labels = labels[:-1]
    cluster = []
    for i, c in enumerate(labels):
        if c == prediction:
            cluster.append(i)
    teams = []
    for index in cluster:
        teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
    return teams

def hierarchical_ward(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "ward")

def hierarchical_complete(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "complete")

def hierarchical_average(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "average")

def hierarchical_single(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "single")

def birch(team_id, year = 2017, n_clusters = 160):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    birch_model = Birch(n_clusters=n_clusters).fit(data_without_year.values)
    prediction = birch_model.predict([team.values[:-1]])
    cluster = []
    for i, c in enumerate(birch_model.labels_):
        if c == prediction:
            cluster.append(i)
    teams = []
    for index in cluster:
        teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
    return teams

def pca(team_id, year = 2017, n_components=43):
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    pca_model = PCA(n_components=n_components)
    pca_model.fit(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
    transformed = pca_model.transform(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
    return transformed

#print(kmeans(1291)) #1243, 1374, 1291,1344 are other ids
#print(spectral(1291))
#print(hierarchical_ward(1291))
#print(hierarchical_complete(1291))
#print(hierarchical_average(1291))
#print(hierarchical_single(1291))
#print(birch(1291))
print(pca(1291))

