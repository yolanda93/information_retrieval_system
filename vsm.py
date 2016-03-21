#!/usr/bin/python
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim import corpora, models, similarities
from operator import itemgetter


sample_corpus = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey"
]


def preprocess_document(doc):
    stopset = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    tokens = wordpunct_tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final = [stemmer.stem(word) for word in clean]
    return final


def create_dictionary(docs):
    pdocs = [preprocess_document(doc) for doc in docs]
    dictionary = corpora.Dictionary(pdocs)
    dictionary.save('/tmp/vsm.dict')
    return dictionary


def get_keyword_to_id_mapping(dictionary):
    print (dictionary.token2id)


def docs2bows(corpus, dictionary):
    docs = [preprocess_document(d) for d in corpus]
    vectors = [dictionary.doc2bow(doc) for doc in docs]
    corpora.MmCorpus.serialize('/tmp/vsm_docs.mm', vectors)
    return vectors


def create_TF_IDF_model(corpus):
    dictionary = create_dictionary(corpus)
    docs2bows(corpus, dictionary)
    loaded_corpus = corpora.MmCorpus('/tmp/vsm_docs.mm')
    tfidf = models.TfidfModel(loaded_corpus)
    return tfidf, dictionary


def launch_query(corpus, q):
    tfidf, dictionary = create_TF_IDF_model(corpus)
    loaded_corpus = corpora.MmCorpus('/tmp/vsm_docs.mm')
    index = similarities.MatrixSimilarity(loaded_corpus, num_features=len(dictionary))
    pq = preprocess_document(q)
    vq = dictionary.doc2bow(pq)
    qtfidf = tfidf[vq]
    sim = index[qtfidf]
    ranking = sorted(enumerate(sim), key=itemgetter(1), reverse=True)
    for doc, score in ranking:
        print ("[ Score = " + "%.3f" % round(score, 3) + "] " + corpus[doc]);
