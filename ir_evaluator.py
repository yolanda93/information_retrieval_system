class IREvaluator(object):
    """description of class"""
    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with:
    #           relevance_docs It contains relevance assessments for each query in MED.QRY
    #################################################################################    
    def __init__(self,relevance_docs,queries):
        self.relevance_docs=relevance_docs
        
        query_id=0
        if len(queries) >1: # Evaluate queries
           for q in queries:
               print("\n-------------------------->Query = " + q ) 
               total_relevant_docs=self.get_total_relevant_docs()
               query_id=query_id+1
        else:
            print("\n-------------------------->Query = " + queries ) 
            self.get_total_relevant_docs(self,queries)


    #################################################################################
    ## @brief   total_relevant_docs
    #  @details This method returns the total relevant documents for a query.
    #  @param   query_id The id of the query
    #  @param   relevance_docs It contains relevance assessments for each query in MED.QRY
    #################################################################################    
    def relevant_doc_retrieved(self,doc):

        return 0

    #################################################################################
    ## @brief   total_relevant_docs
    #  @details This method returns the total relevant documents for a query.
    #  @param   query_id The id of the query
    #################################################################################    
    def get_total_relevant_docs(self): 
        relevant_docs=0   
        query_id=0 
        total_relevant_docs=[]
        for doc in self.relevance_docs:
            if(int(doc[0])==query_id): # the position 0 contains the query ID
              relevant_docs=relevant_docs+1
            if(int(doc[0])>query_id): # relevance docs csv are ordered, we stop to iterate
              query_id=query_id+1
              total_relevant_docs.append(relevant_docs);
              relevant_docs=0               
        return total_relevant_docs


