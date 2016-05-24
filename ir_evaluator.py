class IREvaluator(object):
    """description of class"""
    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with:
    #           relevance_docs It contains relevance assessments for each query in MED.QRY
    #################################################################################    
    def __init__(self,relevance_docs,ranking_query):
        self.relevance_docs=relevance_docs        
        relevants_docs_query=self.get_total_relevant_docs()
      

        if len(ranking_query) >0: # launch queries CAMBIAR!!!
           for q in ranking_query:
               print("\n-------------------------->Query = " + q ) 
               self.evaluate_query(self,ranking_query[q],relevants_docs_query,q)
        else:
            print("\n-------------------------->Query = " + queries ) 
            self.evaluate_query(self,ranking_query[0],relevants_docs_query,0)

        
    
       

   #################################################################################
    ## @brief   evaluate_query
    #  @details This method computes the precision and recall
    #  @param   ranking Ranking result for each 
    #  @param   relevance_docs It contains relevance assessments for each query in MED.QRY
    #################################################################################    
    def evaluate_query(self,ranking,relevants_docs_query):
        [true_positives, false_positives] = self.relevant_doc_retrieved(q,ranking,relevants_docs_query)

        precision = self.get_recall(self,true_positives_retrieved,len(ranking))
        recall = self.get_precision(self,true_positives,false_negatives)


        print("\n-------------------------->The query = " + query_id + "has precision" + precision + "\n")
        print("\n-------------------------->The query = " + query_id + "has recall" + recall + "\n") 
               
        return 


    #################################################################################
    ## @brief   total_relevant_docs
    #  @details This method returns the total relevant documents for a query.
    #  @param   query_id The id of the query
    #  @param   relevance_docs It contains relevance assessments for each query in MED.QRY
    #################################################################################    
    def relevant_doc_retrieved(self,query,ranking,relevants_docs_query):
        true_positives = 0
        false_positives = 0
        for doc in ranking:
           if doc[0] in relevants_docs_query[query]: # position 3 indicates document ID
                true_positives += 1
           else:
                false_positives += 1
        return true_positives,false_positives

    #################################################################################
    ## @brief   total_relevant_docs
    #  @details This method returns the total relevant documents for a query.
    #  @param   query_id The id of the query
    #           relevants_query is a dictionary that stores the query key and the relevant documents IDs
    #################################################################################    
    def get_total_relevant_docs(self): 
        relevant_docs=0   
        query_id=1 
        relevants_query=dict()
        #total_relevant_docs=[]
        relevants_docs_query=[] # stores the relevant docs for a query
        for doc in self.relevance_docs:
            if(int(doc[0])==query_id): # the position 0 contains the query ID
              relevant_docs += 1
              relevants_docs_query.append(doc[2]) # position 3 indicates document ID
            if(int(doc[0])>query_id): # relevance docs csv are ordered, we stop to iterate 
              relevants_query[query_id]=relevants_docs_query       
              query_id += 1
              #total_relevant_docs.append(relevant_docs);
              relevant_docs=0               
        return relevants_docs_query


    #################################################################################
    ## @brief   get_recall
    #  @details A measure of the ability of a system to present all relevant items.
    #  @param   true_positives retrieved documents correctly
    #  @param   false_negatives retrieved documents incorrectly
    #  @param   real_true_positives total of documents that are really relevant 
    #################################################################################    
    def get_recall(self,true_positives,true_negatives,real_true_positives):
        recall=true_positives/real_true_positives
        return recall

    #################################################################################
    ## @brief   get_precision
    #  @details A measure of the ability of a system to present only relevant items.
    #  @param   true_positives retrieved documents correctly
    #  @param   false_negatives retrieved documents incorrectly
    #################################################################################    
    def get_precision(self,true_positives,false_positives):
        relevant_items_retrieved=true_positives+false_positives
        recall=true_positives/relevant_items_retrieved
        return recall
