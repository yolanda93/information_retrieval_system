###################################################################################
## @file      information_retrieval_system.py
#  @brief     The information_retrieval_system.py is a basic information retrieval system  
#             implemented using Python, NLTK and GenSIM.
#  @authors   Yolanda de la Hoz Simon
###################################################################################
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim import corpora, models, similarities
from operator import itemgetter
import abc

###################################################################################
## @class   InformationRetrievalSystem
#  @brief   This class represents the InformationRetrievalSystem, i.e., basic methods 
#           used to preprocess and rank documents according to user queries.
###################################################################################
class IRSystem(object):
    
    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with the parameters introduced by 
    #           the user and execute the query. 
    #################################################################################    
    def __init__(self, corpus, queries):
        __metaclass__ = abc.ABCMeta
        self.corpus=corpus
        self.queries=queries


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
        return dictionary,pdocs

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
    def docs2bows(self,corpus, dictionary, pdocs):
        vectors = [dictionary.doc2bow(doc) for doc in pdocs]
        corpora.MmCorpus.serialize('vsm_docs.mm', vectors) # Save the corpus in the Matrix Market format
        return vectors


    #################################################################################
    ## @brief   create_TF_IDF_model
    #  @details This method creates a weighted TF_IDF matrix to build the vector.
    #  @param   corpus Set of documents to be processed.
    #################################################################################  
    @abc.abstractmethod  
    def create_documents_view(self,corpus):
        return

    #################################################################################
    ## @brief   create_TF_IDF_model
    #  @details This method creates a weighted TF_IDF matrix to build the vector.
    #  @param   corpus Set of documents to be processed.
    #################################################################################  
    @abc.abstractmethod  
    def create_query_view(self,query):
        return

    #################################################################################
    ## @brief   ranking_function
    #  @details This method initializes the class with the parameters introduced by the user
    #           and execute the query. 
    #  @param   corpus Set of documents to be processed.
    #  @param   q Query, a document with the set of relevance words to the user.
    #################################################################################   
    @abc.abstractmethod 
    def ranking_function(self,corpus, q):
        return

    #################################################################################
    ## @brief   launch_query
    #  @details This method initializes the class with the parameters introduced by the user
    #           and execute the query. 
    #  @param   corpus Set of documents to be processed.
    #  @param   q Query, a document with the set of relevance words to the user.
    #################################################################################   
    @abc.abstractmethod 
    def launch_query(self,corpus, q):
        return

class IR_tf_idf(IRSystem):

    def __init__(self,corpus,queries):
        IRSystem.__init__(self,corpus,queries)
        print("\n--------------------------Executing TF IDF information retrieval model--------------------------\n")
        # launch queries
        for q in queries:
          self.ranking_function(corpus,q)

    def create_documents_view(self,corpus):
        dictionary,pdocs = self.create_dictionary(corpus)
        self.docs2bows(corpus, dictionary,pdocs)
        loaded_corpus = corpora.MmCorpus('vsm_docs.mm') # Recover the corpus
        tfidf = models.TfidfModel(loaded_corpus)
        return tfidf, dictionary

    def create_query_view(self,query,dictionary):
        pq = self.preprocess_document(query)
        vq = dictionary.doc2bow(pq)
        return vq

    def ranking_function(self,corpus, q):
        tfidf, dictionary = self.create_documents_view(corpus)
        loaded_corpus = corpora.MmCorpus('vsm_docs.mm')
        index = similarities.MatrixSimilarity(loaded_corpus, num_features=len(dictionary))
        vq=self.create_query_view(q,dictionary)
        qtfidf = tfidf[vq]
        sim = index[qtfidf]
        ranking = sorted(enumerate(sim), key=itemgetter(1), reverse=True)
        for doc, score in ranking:
            print ("[ Score = " + "%.3f" % round(score, 3) + "] " + corpus[doc]);

class IRBoolean(IRSystem):

    def __init__(self,corpus,queries):
        IRSystem.__init__(self,corpus,queries)
        print("\n--------------------------Executing Boolean information retrieval model--------------------------\n")
        print("Not implemented yet")
   
    def create_documents_view(self,corpus):
        """Not implemented yet"""

    def create_query_view(self,query):
        """Not implemented yet"""

    def ranking_function(self,corpus, q):
        """Not implemented yet"""


class IR_tf(IRSystem):

    def __init__(self,corpus,queries):
        IRSystem.__init__(self,corpus,queries)
        print("\n--------------------------Executing TF information retrieval model--------------------------\n")
        print("Not implemented yet")
   
    def create_model(self,corpus):
        """Not implemented yet"""

    def create_query_view(self,query):
        """Not implemented yet"""

    def ranking_function(self,corpus, q):
        """Not implemented yet"""


    
        
        
             


      

