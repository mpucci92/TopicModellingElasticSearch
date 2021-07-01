from sentence_transformers import SentenceTransformer, models
import umap
import numpy as np
import pandas as pd

def transformerModel(data,path_to_model,seq_length):

    word_embedding_model = models.Transformer(path_to_model, max_seq_length=seq_length)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    embeddings = model.encode(data)

    return embeddings

def umapEmbeddings(neighbors,components,metric,embeddings):
    umap_embeddings = umap.UMAP(n_neighbors=neighbors, # 15
                                n_components=components,  # 2 cosine
                                min_dist=0.0,
                                metric=metric).fit_transform(embeddings)
    return umap_embeddings

