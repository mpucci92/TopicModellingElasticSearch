from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np
from getUmapEmbeddings import *
from hdbscanClusters import *
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def clusterScoring(dataframe, titleX, titleY, titleLabels):

    X1 = np.array(list(zip(dataframe[titleX], dataframe[titleY])))
    X2 = np.array(dataframe[titleLabels])

    # daviesScore = (davies_bouldin_score(X1,X2))
    try:
        silhouetteScore = silhouette_score(X1, X2, metric='euclidean')
    except Exception as e:
        silhouetteScore = -1000

    # print(daviesScore)
    return silhouetteScore

def clusterSelection(df):
    path_to_model = r'E:\Pretrained Models\distilbert-base-nli-stsb-mean-tokens'

    scoringFrame = pd.DataFrame()
    nCompParameters = []
    metricParamters = []
    csmParameters = []
    cseParameters = []
    mcsParameters= []
    silhouetteScoreParameters = []

    n_components = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    metrics = ['euclidean', 'cosine', 'correlation', 'manhattan', 'chebyshev', 'minkowski']

    cluster_selection_method = ['eom', 'leaf']
    cluster_selection_epsilon = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    min_cluster_size = [2, 5, 8, 10, 12, 15, 20,25,30]

    data = list(df.title)
    embeddings = transformerModel(data, path_to_model, 256)
    for ncomponent in n_components:
        for metric in metrics:
            umap_embeddings = umapEmbeddings(ncomponent, 2, metric, embeddings)

            for mcs in min_cluster_size:
                for csm in cluster_selection_method:
                    for cse in cluster_selection_epsilon:
                        cluster = topicClusters(mcs, 'euclidean', csm,cse, umap_embeddings)

                        result = pd.DataFrame(umap_embeddings, columns=['x', 'y'])
                        result['labels'] = cluster.labels_

                        silScore = clusterScoring(result,'x','y','labels')

                        nCompParameters.append(ncomponent)
                        metricParamters.append(metric)
                        csmParameters.append(csm)
                        cseParameters.append(cse)
                        mcsParameters.append(mcs)
                        silhouetteScoreParameters.append(silScore)


    scoringFrame['n_components_UMAP'] = nCompParameters
    scoringFrame['metrics_UMAP'] = metricParamters
    scoringFrame['mcs'] = mcsParameters
    scoringFrame['csm'] = csmParameters
    scoringFrame['cse'] = cseParameters
    scoringFrame['silscore'] = silhouetteScoreParameters

    scoringFrame = scoringFrame.sort_values(by=['silscore'], ascending=True)

    return scoringFrame



df = pd.read_csv(r"E:\test\dataES.csv")
print(clusterSelection(df))