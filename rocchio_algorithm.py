class RocchioAlgorithm(object):
    """description of class"""
    #################################################################################
    ## @brief   Constructor
    #  @details This method initializes the class with:
    #           user_improvement ID's of the relevant documents
    #################################################################################    
    def __init__(self,query,corpus,relevance_judgments,ir):
        dictionary,pdocs = ir.create_dictionary(corpus)
        queryVector = ir.create_query_view(query,dictionary)        
        query_mod = self.execute_rocchio(dictionary,relevance_judgments, queryVector, 1, .75, .15, 0)
        self.new_query = self.getNewQuery(query, query_mod, dictionary)


    def getQueryVector(self,query,dictionary):
	    queryVector = [0] * len(dictionary)
	    for word in query.split():
		    pos = dictionary[word]
		    queryVector[pos] = queryVector[pos] + 1
	    return queryVector	

    def execute_rocchio(self,dictionary,relevance, queryVector, alpha, beta, gamma, method=0):
	    relDocs = [relevance[i] for i in range(len(relevance)) if relevance[i] > 0.0]
	    nonRelDocs = [relevance[i] for i in range(len(relevance)) if relevance[i] <= 0.0]

	    term1 = [alpha*i for i in queryVector]
	    term2 = [float(beta)/len(relDocs) * i[1] for i in relDocs]
	    term3 = [-float(gamma)/len(nonRelDocs) * i[1] for i in nonRelDocs]
	
	    modQueryVec = [sum(wordCol) for wordCol in zip(term1,term2,term3)]
	    return modQueryVec

    def getKey(self,item):
	    return item[1]

    def getNewQuery(self,query, queryMod, dictionary):
	    # find 2 new words with maximum value
	    temp = queryMod[:]
	    temp.sort(reverse = True)
	    count = 0
	    for element in temp:
		    pos = queryMod.index(element)
		    word = dictionary[pos]
		    if word not in query:
			    query = query + ' ' + word
			    count = count + 1
			    if count==2:
				    break

	    return query

