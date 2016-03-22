#!/usr/bin/python
###################################################################################
## @file      information_retrieval_system.py
#  @brief     The information_retrieval_system.py is a basic information retrieval system  
#             implemented using Python, NLTK and GenSIM.
#  @authors   Yolanda de la Hoz Simón
###################################################################################
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

###################################################################################
## @class   InformationRetrievalSystem
#  @brief   This class represents the InformationRetrievalSystem, i.e., basic methods used to
#           preprocess and rank documents according to user queries.
###################################################################################
class InformationRetrievalSystem(object):


    #################################################################################
    ## @brief   preprocess_document
    #  @details This method return the taxonomy of keywords for the given document.
    #  @param   doc The document to be preprocessed
    #################################################################################    
    def preprocess_document(doc):
        stopset = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        tokens = wordpunct_tokenize(doc)
        clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
        final = [stemmer.stem(word) for word in clean]
        return final


    #################################################################################
    ## @brief   create_dictionary
    #  @details This method creates a dictionary based on the taxonomy of keywords for each document.
    #  @param   docs The documents to be preprocessed
    #################################################################################    
    def create_dictionary(docs):
        pdocs = [preprocess_document(doc) for doc in docs]
        dictionary = corpora.Dictionary(pdocs)
        dictionary.save('/tmp/vsm.dict')
        return dictionary

    #################################################################################
    ## @brief   get_keyword_to_id_mapping
    #  @details This method prints the tokens id (word counts) for the given dictionary.
    #  @param   dictionary The dictionary with the documents keywords.
    #################################################################################    
    def get_keyword_to_id_mapping(dictionary):
        print (dictionary.token2id)


    #################################################################################
    ## @brief   docs2bows
    #  @details This method converts document (a list of words) into the bag-of-words
    #  format = list of (token_id, token_count) 2-tuples.
    #  @param   corpus Set of documents to be processed.
    #  @param   dictionary The dictionary with the documents keywords.
    #################################################################################    
    def docs2bows(corpus, dictionary):
        docs = [preprocess_document(d) for d in corpus]
        vectors = [dictionary.doc2bow(doc) for doc in docs]
        corpora.MmCorpus.serialize('/tmp/vsm_docs.mm', vectors) # Save the corpus in the Matrix Market format
        return vectors


    #################################################################################
    ## @brief   create_TF_IDF_model
    #  @details This method creates the TF IDF model to build the vector.
    #  @param   corpus Set of documents to be processed.
    #################################################################################    
    def create_TF_IDF_model(corpus):
        dictionary = create_dictionary(corpus)
        docs2bows(corpus, dictionary)
        loaded_corpus = corpora.MmCorpus('/tmp/vsm_docs.mm')
        tfidf = models.TfidfModel(loaded_corpus)
        return tfidf, dictionary


    #################################################################################
    ## @brief   launch_query
    #  @details This method initializes the class with the parameters introduced by the user
    #           and execute the query. 
    #  @param   corpus Set of documents to be processed.
    #  @param   q Query, a document with the set of relevance words to the user.
    #################################################################################    
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


    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with the parameters introduced by the user
    #           and execute the query. 
    #################################################################################    
    def __init__(self):
