import matplotlib.pyplot as plot
class IREvaluator(object):
    """description of class"""
    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with:
    #           relevance_docs It contains relevance assessments for each query in MED.QRY
    #           ranking_query  
    #################################################################################    
    def __init__(self,relevance_docs,ranking_query):
        self.relevance_docs=relevance_docs        
        relevants_docs_query=self.get_total_relevant_docs()
      
        query_id=1
        if len(ranking_query) >1: 
           for q in ranking_query-1:
               print("\n-------------------------->Query = " + str(query_id) ) 
               self.evaluate_query(ranking_query[q],relevants_docs_query,query_id)
               query_id += 1
        else:
            print("\n-------------------------->Query = " + str(query_id) ) 
            self.evaluate_query(ranking_query[1],relevants_docs_query,1)


   #################################################################################
    ## @brief   evaluate_query
    #  @details This method computes the precision and recall
    #  @param   ranking Ranking result for each query
    #  @param   relevance_docs It contains relevance assessments for each query in MED.QRY
    #################################################################################    
    def evaluate_query(self,ranking,relevants_docs_query,query_id):
        [true_positives, false_positives] = self.relevant_doc_retrieved(query_id,ranking,relevants_docs_query)

        recall = self.get_recall(true_positives,len(relevants_docs_query[query_id]))
        precision = self.get_precision(true_positives,false_positives)


        print(" Precision: " + str(precision) + "\n")
        print(" Recall:  "  +  str(recall) + "\n") 

        plot_results(recall, precision)
               
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
           if str(doc[0]) in relevants_docs_query[query]: # position 3 indicates document ID
                true_positives += 1
           else:
                false_positives += 1
        return true_positives,false_positives

    #################################################################################
    ## @brief   total_relevant_docs
    #  @details This method returns the total relevant documents for a query.
    #  @param   relevants_docs_query is a dictionary that stores the query key and the relevant documents IDs
    #################################################################################    
    def get_total_relevant_docs(self): 
        query_id=1 
        relevants_query=dict()
        relevants_docs_query=[] # stores the relevant docs for a query
        for doc in self.relevance_docs:
            if(int(doc[0])==query_id): # the position 0 contains the query ID
              relevants_docs_query.append(doc[2]) # position 3 indicates document ID
            if(int(doc[0])>query_id): # relevance docs csv are ordered, we stop to iterate 
              relevants_query[query_id]=relevants_docs_query  
              relevants_docs_query=[] # clean     
              query_id += 1   
        return relevants_query


    #################################################################################
    ## @brief   get_recall
    #  @details A measure of the ability of a system to present all relevant items.
    #  @param   true_positives retrieved documents correctly
    #  @param   false_negatives retrieved documents incorrectly
    #  @param   real_true_positives total of documents that are really relevant 
    #################################################################################    
    def get_recall(self,true_positives,real_true_positives):
        recall=float(true_positives)/float(real_true_positives)
        return recall

    #################################################################################
    ## @brief   get_precision
    #  @details A measure of the ability of a system to present only relevant items.
    #  @param   true_positives retrieved documents correctly
    #  @param   false_negatives retrieved documents incorrectly
    #################################################################################    
    def get_precision(self,true_positives,false_positives):
        relevant_items_retrieved=true_positives+false_positives
        precision=float(true_positives)/float(relevant_items_retrieved)
        return precision
    
    
    #################################################################################
    ## @brief   plot_results
    #  @details plot the result of evaluate each query
    #  @param   recall retrieved documents correctly
    #  @param   precision retrieved documents incorrectly
    #################################################################################   
    def plot_results(recall, precision):
        plot.plot(recalls, precisions)
        plot.ylabel('precision')
        plot.xlabel('recall')
        plot.draw()

        path_save = raw_input("Please, provide the path where the results should be saved \n")
        if len(path_save) >0: 
            if os.path.exists(path_save):
               plt.savefig(path_save)
            else:
               os.makedirs(path_save)

        #show results
        plot.show()
        plot.close()