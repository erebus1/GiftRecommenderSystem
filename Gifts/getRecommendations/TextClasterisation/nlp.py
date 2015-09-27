from StopWords import stop_list
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim import corpora
import sklearn.cluster
from collections import defaultdict



def stemm(tokens):
    stemmer = SnowballStemmer("english")
    return [stemmer.stem(token) for token in tokens]


def remove_stop_words(texts):
    stop = stopwords.words('english') + stop_list
    return [[token for token in tokens if token not in stop] for tokens in texts]


def remove_unique_words(texts, min_frequency=11):
    # remove words that appear less than min_frequency times

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    return [[token for token in text if frequency[token] >= min_frequency]
            for text in texts]

def clean_texts_simple(texts):
    texts = [nltk.word_tokenize(text) for text in texts]  # tokenise
    texts = [[word.lower() for word in text] for text in texts]  # lower case
    texts = [stemm(text) for text in texts]  # stemm
    texts = remove_stop_words(texts)  # remove stop words
    return texts

def clean_texts(texts):
    texts = [nltk.word_tokenize(text) for text in texts]  # tokenise
    texts = [[word for word in text if len(word) > 2] for text in texts]  # remove len < 3
    texts = [[word.lower() for word in text] for text in texts]  # lower case
    texts = [stemm(text) for text in texts]  # stemm
    texts = remove_stop_words(texts)  # remove stop words
    texts = remove_unique_words(texts)  # remove words, that presents less than n times
    return texts


def make_corpus(texts):
     # convert text in to spare matrix
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(title) for title in texts]
    corpus = [[(token[0], 1) for token in title] for title in corpus]

    # each title represented by n-dim vector
    corpus_new = [[token[0] for token in title] for title in corpus]
    number_of_tokens = len(dictionary.token2id)
    corpus_new = [[1 if i in title else 0 for i in range(number_of_tokens)] for title in corpus_new]
    return corpus_new, dictionary



def get_prediction(titles, n_clusters=10):

    titles = clean_texts(titles)
    corpus, dictionary = make_corpus(titles)  # represent each title in n-dim vector

    # Train model

    kMeans = sklearn.cluster.KMeans(n_clusters=n_clusters)
    prediction = kMeans.fit_predict(corpus)
    return prediction




