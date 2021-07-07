from sklearn.feature_extraction.text import CountVectorizer
from main import *


def c_tf_idf(documents, m, ngram_range=(1, 1)):
    """
    ngram_range(x,y): indicates the ngram to find within topics
    """

    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count

def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=5):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}

    return top_n_words

def extract_topic_sizes(df):
    topic_sizes = (df.groupby(['Topic'])
                     .Doc
                     .count()
                     .reset_index()
                     .rename({"Topic": "Topic", "Doc": "Size"}, axis='columns')
                     .sort_values("Size", ascending=False))

    return topic_sizes

def topicDataFrame(data,cluster):
    docs_df = pd.DataFrame(data, columns=["Doc"])
    docs_df['Topic'] = cluster.labels
    docs_df['Doc_ID'] = range(len(docs_df))
    docs_per_topic = docs_df.groupby(['Topic'], as_index=False).agg({'Doc': ' '.join})

    tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(data))

    top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=5)

    topic_number = []
    keywords_topics = []
    tfScore = []
    n = 5

    for key in list(top_n_words.keys()):

        if key != -1:
            for j, element in enumerate(top_n_words[key][:n]):
                if element[1] > 0.01:
                    if j != n:
                        topic_number.append(key)
                        keywords_topics.append(element[0])
                        tfScore.append(element[1])

    df = pd.DataFrame()
    df['topic'] = topic_number
    df['keywords'] = keywords_topics
    df['score'] = tfScore
    df = df.sort_values(by=['topic']).reset_index(drop=True)

    return df