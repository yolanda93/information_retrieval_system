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
import re
import sys

###################################################################################
## @class   InformationRetrievalSystem
#  @brief   This class represents the InformationRetrievalSystem, i.e., basic methods 
#           used to preprocess and rank documents according to user queries.
###################################################################################
class InformationRetrievalSystem():
    
    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with the parameters introduced by 
    #           the user and execute the query. 
    #################################################################################    
    def __init__(self):
        print("constructor")


    #################################################################################
    ## @brief   preprocess_document
    #  @details This method return the taxonomy of keywords for the given document.
    #  @param   doc The document to be preprocessed
    #################################################################################    
    def preprocess_document(self,doc):
        stopset = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        tokens = wordpunct_tokenize(doc) # split text on whitespace and punctuation
        clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
        final = [stemmer.stem(word) for word in clean]
        return final


    #################################################################################
    ## @brief   create_dictionary
    #  @details This method creates a dictionary based on the taxonomy of keywords for each document.
    #  @param   docs The documents to be preprocessed
    #################################################################################    
    def create_dictionary(self,docs):
        pdocs = [self.preprocess_document(doc) for doc in docs]
        dictionary = corpora.Dictionary(pdocs)
        dictionary.save('vsm.dict')
        return dictionary

    #################################################################################
    ## @brief   get_keyword_to_id_mapping
    #  @details This method prints the tokens id (word counts) for the given dictionary.
    #  @param   dictionary The dictionary with the documents keywords.
    #################################################################################    
    def get_keyword_to_id_mapping(self,dictionary):
        print (dictionary.token2id)

    #################################################################################
    ## @brief   docs2bows
    #  @details This method converts document (a list of words) into the bag-of-words
    #  format = list of (token_id, token_count) 2-tuples.
    #  @param   corpus Set of documents to be processed.
    #  @param   dictionary The dictionary with the documents keywords.
    #################################################################################    
    def docs2bows(self,corpus, dictionary):
        docs = [self.preprocess_document(d) for d in corpus]
        vectors = [dictionary.doc2bow(doc) for doc in docs] # each vector is an histogram of terms of document
        corpora.MmCorpus.serialize('vsm_docs.mm', vectors) # Save the corpus in the Matrix Market format
        return vectors


    #################################################################################
    ## @brief   create_TF_IDF_model
    #  @details This method creates a weighted TF_IDF matrix to build the vector.
    #  @param   corpus Set of documents to be processed.
    #################################################################################    
    def create_TF_IDF_model(self,corpus):
        dictionary = self.create_dictionary(corpus)
        self.docs2bows(corpus, dictionary)
        loaded_corpus = corpora.MmCorpus('vsm_docs.mm') # Recover the corpus
        tfidf = models.TfidfModel(loaded_corpus)
        return tfidf, dictionary


    #################################################################################
    ## @brief   launch_query
    #  @details This method initializes the class with the parameters introduced by the user
    #           and execute the query. 
    #  @param   corpus Set of documents to be processed.
    #  @param   q Query, a document with the set of relevance words to the user.
    #################################################################################    
    def launch_query(self,corpus, q):
        tfidf, dictionary = self.create_TF_IDF_model(corpus)
        loaded_corpus = corpora.MmCorpus('vsm_docs.mm')
        index = similarities.MatrixSimilarity(loaded_corpus, num_features=len(dictionary))
        pq = self.preprocess_document(q)
        vq = dictionary.doc2bow(pq)
        qtfidf = tfidf[vq]
        sim = index[qtfidf] # get similarities between the query and all index documents
        ranking = sorted(enumerate(sim), key=itemgetter(1), reverse=True) # Documents most similar to the query are arranged first 
        for doc, score in ranking: 
            print ("[ Score = " + "%.3f" % round(score, 3) + "] " + corpus[doc]);


    #################################################################################
    ## @brief   preprocess_input
    #  @details This method reads user input and transform it into a list
    #  @param   user_input The input given by the user
    #################################################################################  
    def preprocess_userinput(self,user_input):
        if "/" or "\\" in user_input: # the user has provided a file path with a set of texts
            try:
               list_texts = re.split(".I \d*\n.W\n",open(user_input).read())[1:] # Split text file with the delimiter, erase first delimiter
               return list_texts
            except IOError:
               print query_input + " - No such file or directory"
               sys.exit(1)
        return user_input # the user has provided a query or a text    


####################################################################################################################### 
## @brief The main function that enables the user to launch queries
####################################################################################################################### 
if __name__ == '__main__':
    
      corpus_input = raw_input("Write a text or enter the corpus path: ") 
      query_input = raw_input("Write a query or enter a document path with a set of queries: ") 

      ir = InformationRetrievalSystem()
      corpus_text=ir.preprocess_userinput(corpus_input)
      query_text=ir.preprocess_userinput(query_input)

      for q in query_text:
          ir.launch_query(corpus_text,q)


    
        
        
             


      

