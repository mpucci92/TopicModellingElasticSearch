# McGill University - Final Project  
Topic Modelling Project for YCNG 229 - Neural Networks & Deep Learning Course

This repository is for individuals who would like to find clusters from titles that are presumed to be relatively similar to each other. The objective of this project was to cluster similar financial news headlines in order to streamline prevalent topics coming from over 280 different financial news sources. 

  * Set up a git repo on github
  * Use git repo to spawn local flask web application that clusters financial news data coming from an ElasticSearch Cluster
  * To display clusters in interactive circle Bokeh plot 

Prerequisites:

* python >= 3.8.5
* conda installed
* See Environment.yml file for required python packages

# Code Organization 
 * `app.py`: This file contains the main for the Flask server. It is also the entrypoint of the app. It contains 1 entrypoint that takes in the 'index','keyword','start date' and 'end date' as parameters.
 * `CONFIG.py`: This file is used to load the text file containing the ElasticSearch IP address - used when querying for news data to be used in the topic model.
 * `GenerateDataset.py`: This file is used to generate dataframe structure based on a particular ElasticSearch Query.
 * `getData.py`: This file is used to retrieve the raw news headlines data from ElasticSearch cluster - Data can be retrieved from the "news" index or the "tweets" index. 
 * `getUmapEmbeddings.py`: This file is used to generate UMAP embeddings from embeddings from distilbert outputs.
 * `hdbscanClusters.py`: This file is used to generate clusters from the UMAP embeddings - cluster function is defined in this script.
 * `main.py`: Main script used to take in parameters and output topic clustered bokeh plot local html file. 
 * `ParameterTuningClusters.py`: Script to tune hyperparameters for UMAP embeddings and hdbscan clusters - goal is to maximize silhouette score for clusters. 
 * `SearchAPI.py`: Script used to perform general searches on ElasticSearch Cluster
 * `textPreprocessing.py`: Script used to preprocess text data - news headlines before generating embeddings
 * `TopicBokehPlot.py`: Script used that contains bokeh plot function used to generate bokeh plot with user defined parameters. 

# APP workflow
The app is using a flask server to process the queries. When the server receive a query on '/model/`<index>/<keyword>/<startTime>/<endTime>'` where `<index>` is an elasticsearch index, where `<keyword>` is a keyword for specific news retrieval, where `<startTime>` is the start time period for elasticsearch news query and where `<endTime>` is the end time period for elasticsearch news query.
 
 Note: 
 * `<index>`:
   * news: retrieve data from financial news articles
   * tweets: retrieve data from financial twitter handles
 * `<keyword>`:
   * empty: 'empty' will retrieve ALL news for a given period
 * `<startTime>`:
   * Format: YYYY-MM-DDTHH:MM:SS 
 * `<endTime>`:
   * Format: YYYY-MM-DDTHH:MM:SS 
 
The following will:
1. Run the app.py file to load up flask web server and then input into browser corresponding URL: `http://127.0.0.1:8080/model/<index>/<keyword>/<startTime>/<endTime>'`
2. Pass the flask parameters to elasticsearch query object. Check if a model exists for this specific ticker
    - If the parameters are defined with the correct format - financial data will be retrieved from elasticsearch cluster. 
2. The data will then be passed to textPreprocessing function and output will be a list of title. 
3. The list of titles will then go through distilbert model and generate text embeddings. 
4. Distilbert Embeddings will then be dimension reduced through UMAP embeddings implmentation. 
5. HDBSCAN clustering will occur on 2D embbedings and Bokeh topic model plot will be made on top of the UMAP Embeddings and the HDBSCAN cluster labels. 

 
# Example of Bokeh Plot Topic Modelling Clusters
![Bokehplot](https://user-images.githubusercontent.com/42786192/124517259-88dbfb00-ddb1-11eb-8194-4b2cf3405633.png)

