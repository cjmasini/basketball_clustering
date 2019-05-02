from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering, Birch
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import numpy as np
import util.load_data as ld

def clustering(team_id, year = 2017, n_clusters = 91, func=None, fittable=None, pca_flag=False, pca_components=10, linkage="ward"):
    # Dictionary by year containing dataframes
    # Up to 68 teams per year
    if func is not None and fittable is not None:
        data = ld.load_normalized_data_without_year(year)
        data["team_id_copy"] = data.index
        data_without_year = data.drop("year", axis=1)
        data_without_year = data_without_year.drop("team_id_copy", axis=1)
        latest = ld.load_normalized_year_data(year)
        team = ld.load_normalized_team_data(team_id, year)
        if pca_flag:
            fit_data, fit_team = pca(team_id, year = year, n_components=pca_components)
        else:
            fit_data = data_without_year.values
            fit_team = team.values[:-1]
        if fittable:
            if func==KMeans:
                model = func(n_clusters=n_clusters, random_state=0).fit(data_without_year.values)
            else:
                model = func(n_clusters=n_clusters).fit(data_without_year.values)
            prediction = model.predict([team.values[:-1]])
            cluster = []
            for i, c in enumerate(model.labels_):
                if c == prediction:
                    cluster.append(i)
        else:
            if func==AgglomerativeClustering:
                labels = AgglomerativeClustering(n_clusters=n_clusters,linkage=linkage).fit_predict(np.concatenate((fit_data,[fit_team]),0))
            elif func==SpectralClustering:
                labels = func(n_clusters=n_clusters, random_state=0).fit_predict(np.concatenate((fit_data,[fit_team]),0))
            else:
                labels = func(n_clusters=n_clusters).fit_predict(np.concatenate((fit_data,[fit_team]),0))
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

def pca(team_id, year = 2017, n_components=10):
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    pca_model = PCA(n_components=n_components)
    pca_model.fit(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
    transformed = pca_model.transform(np.concatenate((data_without_year.values,[team.values[:-1]]),0))
    return transformed[:-1], transformed[-1]

def kmeans(team_id, year = 2017, n_clusters = 91):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=KMeans, fittable=True)

def spectral(team_id, year = 2017, n_clusters = 160):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=SpectralClustering, fittable=False)

def hierarchical(team_id, year = 2017, n_clusters = 160, linkage="ward"):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=AgglomerativeClustering, fittable=False, linkage=linkage)

def hierarchical_ward(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "ward")

def hierarchical_complete(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "complete")

def hierarchical_average(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "average")

def hierarchical_single(team_id, year = 2017, n_clusters = 160):
    return hierarchical(team_id, year, n_clusters, "single")

def birch(team_id, year = 2017, n_clusters = 160):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=Birch, fittable=True)

def pca_kmeans(team_id, year = 2017, n_clusters = 91):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=KMeans, fittable=True, pca_flag=True)

def pca_spectral(team_id, year = 2017, n_clusters = 160):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=SpectralClustering, fittable=False, pca_flag=True)

def pca_hierarchical(team_id, year = 2017, n_clusters = 160, pca_flag=True, linkage="ward"):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=AgglomerativeClustering, fittable=False, pca_flag=True, linkage=linkage)

def pca_hierarchical_ward(team_id, year = 2017, n_clusters = 160):
    return pca_hierarchical(team_id, year, n_clusters, linkage="ward")

def pca_hierarchical_complete(team_id, year = 2017, n_clusters = 160):
    return pca_hierarchical(team_id, year, n_clusters, linkage="complete")

def pca_hierarchical_average(team_id, year = 2017, n_clusters = 91):
    return pca_hierarchical(team_id, year, n_clusters, linkage="average")

def pca_hierarchical_single(team_id, year = 2017, n_clusters = 91):
    return pca_hierarchical(team_id, year, n_clusters, linkage="single")

def pca_birch(team_id, year = 2017, n_clusters = 160):
    return clustering(team_id, year = year, n_clusters = n_clusters, func=Birch, fittable=True, pca_flag=True)

def kneighbors(team_id, year = 2017, n_neighbors=10, pca_flag=False, pca_components=10):
    data = ld.load_normalized_data_without_year(year)
    data["team_id_copy"] = data.index
    data_without_year = data.drop("year", axis=1)
    data_without_year = data_without_year.drop("team_id_copy", axis=1)
    latest = ld.load_normalized_year_data(year)
    team = ld.load_normalized_team_data(team_id, year)
    if pca_flag:
        fit_data, fit_team = pca(team_id, year = year, n_components=pca_components)
    else:
        fit_data = data_without_year.values
        fit_team = team.values[:-1]
    cluster = NearestNeighbors(n_neighbors=n_neighbors).fit(fit_data).kneighbors([fit_team])[1][0]
    teams = []
    for index in cluster:
        teams.append((int(data.iloc[index].team_id_copy),data.iloc[index].year))
    return teams

def pca_kneighbors(team_id, year = 2017, n_neighbors=10, n_components=10):
    return kneighbors(team_id, year, n_neighbors, True, n_components)

#print(kmeans(1291)) #1243, 1374, 1291,1344 are other ids
#print(spectral(1291))
#print(hierarchical_ward(1291))
#print(hierarchical_complete(1291))
#print(hierarchical_average(1291))
#print(hierarchical_single(1291))
#print(birch(1291))
#print(pca_kmeans(1291))
#print(kneighbors(1291))

