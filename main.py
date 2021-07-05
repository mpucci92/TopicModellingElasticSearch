import nltk
from elasticsearch import Elasticsearch
from textPreprocessing import *
from getData import *
from getUmapEmbeddings import *
from hdbscanClusters import *
from SearchAPI import *
from CONFIG import configFile
from GenerateDataset import *
from gensim.parsing.preprocessing import remove_stopwords
from sentence_transformers import SentenceTransformer, models
import umap
import hdbscan
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from TopicBokehPlot import *
from sklearn.metrics import silhouette_score

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


def clusterScoring(dataframe, titleX, titleY, titleLabels):
    scoringFrame = pd.DataFrame()

    X1 = np.array(list(zip(dataframe[titleX], dataframe[titleY])))
    X2 = np.array(dataframe[titleLabels])

    # daviesScore = (davies_bouldin_score(X1,X2))
    silhouetteScore = silhouette_score(X1, X2, metric='euclidean')

    # print(daviesScore)
    print(silhouetteScore)

def main(index,keyword,start_time,end_time):
    path_to_model = r'E:\Pretrained Models\distilbert-base-nli-stsb-mean-tokens'
    # index = 'news'
    # keyword = ''
    # start_time = 'now-24h'
    # end_time = 'now'

    # Generate Dataframe and join all titles and preprocess #
    dfTicker = themedf(index, keyword, start_time, end_time)
    cleanSentence = []

    if index == 'news':
        for title in dfTicker.title:
            cleanSentence.append(remove_stopwords(textPreprocess(title)))
    else:
        for title in dfTicker.tweet:
            cleanSentence.append(remove_stopwords(textPreprocess(title)))

    cleanSentence = (list(set(cleanSentence)))
    data = cleanSentence

    #    # Model Parameters #
    embeddings = transformerModel(data, path_to_model, 256)
    umap_embeddings = umapEmbeddings(15, 2, 'cosine', embeddings)
    cluster = topicClusters(10, 'euclidean', 'leaf', 0.1, umap_embeddings)

    result = pd.DataFrame(umap_embeddings, columns=['x', 'y'])
    result['labels'] = cluster.labels_

    return result,data


if __name__ == '__main__':

    # Parameters #
    path_to_model = r'E:\Pretrained Models\distilbert-base-nli-stsb-mean-tokens'
    index = 'news'
    keyword = ''
    start_time = 'now-24h'
    end_time = 'now'

    # Generate Dataframe and join all titles and preprocess #
    dfTicker = themedf(index, keyword, start_time, end_time)
    cleanSentence = []

    if index == 'news':
        for title in dfTicker.title:
            cleanSentence.append(remove_stopwords(textPreprocess(title)))
    else:
        for title in dfTicker.tweet:
            cleanSentence.append(remove_stopwords(textPreprocess(title)))

    cleanSentence = (list(set(cleanSentence)))
    data = cleanSentence

    #    # Model Parameters #
    embeddings = transformerModel(data, path_to_model, 256)
    umap_embeddings = umapEmbeddings(15, 2, 'cosine',embeddings)
    cluster = topicClusters(2, 'euclidean', 'leaf',0.1, umap_embeddings)

    result = pd.DataFrame(umap_embeddings, columns=['x', 'y'])
    result['labels'] = cluster.labels_

    # Uncomment to generate bokeh plot:
    generateBokeh(result, data)
