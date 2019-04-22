from sklearn.cluster import KMeans, SpectralClustering
import numpy as np
import util.load_data as ld

def kmeans(team_id=0,n_clusters=32):
    # Dictionary by year containing dataframes
    # 68 teams per year
    year = 2017

    data = ld.load_normalized_data_as_dataframe()
    latest = ld.load_normalized_year_as_dataframe(year)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data.values)
    prediction = kmeans.predict([latest.values[team_id]])
    cluster = []
    for i, c in enumerate(kmeans.labels_):
        if c == prediction:
            cluster.append(i)
    teams = []
    for index in cluster:
        year = 2003 + index//68
        num = index%68
        teams.append((year,num))
    return teams


print(kmeans())
