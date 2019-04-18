# Predicting March Madness using clustering
This project aims to predict the results of march madness using various clustering based methods


## data 
### data 
This subfolder contains all of the unproccessed data used in this project
#### kaggle_raw
This folder contains all of the raw data taken from kaggle. This data contains all game information and is used to generate most of the advanced stats used and the structure/layout of the tournament
#### kenpom_raw
This folder contains all of the raw data taken from kenpom, found at [https://kenpom.com/]
#### kenpom_processed
This folder contains all of the data taken from kenpom. In order to combine this efficieny data with the kaggle dataset, some duplicate aspects of the raw data were removed and team id's were converted to match those in the kaggle dataset
### data_matrices
This subfolder contains all of the advanced statistics and useful data extracted from the raw datasets
#### team_stats
This folder contains the aggregated basic statistics (things like total points scored, or total shots taken from 3) that were compiled from the raw data. This ddata is used to contsruct the tournament_matrices folder
#### tournament_matrices
This folder contains game and team statistics for each tournament game. This data is used in the testing folder
#### tournament_stats
This folder contains all of the advanced and basic statistics used for clustering. The data is limited to a list of team ids for tournament teams and all of the features describing them. It can be loaded using functions found in the util folder
## preprocessing
This folder contains all of the code used to process the raw data into the tournament_stats matrices
## testing
This folder contains all of the code needed to test various clustering models accuracy
### util
This folder contains any classes that might be useful for testing the code
