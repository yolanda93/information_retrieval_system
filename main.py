#!/usr/bin/python
import ir_system    
import ir_evaluator
import sys
import re
import os
import csv
#################################################################################
## @brief   preprocess_input
#  @details This method reads user input and transform it into a list
#  @param   user_input The input given by the user
#################################################################################  
def preprocess_userinput(user_input):
    path=user_input[:-8]  # Erase the file name and keep the path
    if os.path.exists(path): # the user has provided a file path with a set of texts
       try:
           list_texts = re.split(".I \d*\n.W\n",open(user_input).read())[1:] # Split text file with the delimiter, erase first delimiter
           return list_texts
       except IOError:
            print user_input + " - No such file or directory"
            sys.exit(0)
    return user_input # the user has provided a query or a text    

#################################################################################
## @brief   create_ir_system
#  @details This method creates an information retrieval system with the model 
#           chosen by the user
#  @param   irmodel_choice The id of the information retrieval model chosen by the user
#################################################################################  
def create_ir_system(irmodel_choice,corpus,query):
    if irmodel_choice == 0:
       return ir_system.IRBoolean(corpus,query)
    elif irmodel_choice == 1:
       return ir_system.IR_tf(corpus,query)
    elif irmodel_choice == 2:
       return ir_system.IR_tf_idf(corpus,query)


####################################################################################################################### 
## @brief The main function that enables the user to launch queries
####################################################################################################################### 
if __name__ == '__main__':
   
      print("--------------------------------------------------------\n")
      print("------------ Project: Information Retrieval System\n")
      print("------------ Course:  Data Science Master - Technical University of Madrid\n")
      print("------------ Subject: Information Extraction, Retrieval and Intregation\n")
      print("------------ Author:  Yolanda de la Hoz Simon\n")
      print("--------------------------------------------------------\n")

      corpus_input = raw_input("Write a text or enter the corpus path:\n") 
      corpus_text=preprocess_userinput(corpus_input)
    
      query_input = raw_input("Write a query or enter a document path with a set of queries:\n") 
      query_text=preprocess_userinput(query_input)

    
      print("\n The available models are: \n 0:Boolean\n 1:TF\n 2:TF-IDF\n \n")
      irmodel_choice = raw_input("Please, choose an information retrieval model by entering the id of the model:\n") 

      ir = create_ir_system(int(irmodel_choice),corpus_text,query_text)
      
      irevaluator_choice = raw_input("Do you want to execute the performance evaluation of the IR system selected (YES/NO)? \n")
   
      if((irevaluator_choice=="YES") | (irevaluator_choice=="yes") ):
         relevances_input = raw_input("Write the directory path with the document relevances:\n") 
         with open(relevances_input, 'rb') as csvfile:
              spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
              relevances=[]
              for row in spamreader:
                  relevances.append(row)

         ir_evaluator.IREvaluator(relevances,ir.ranking_query)
      
     
      rocchio_choice = raw_input("Do you want to execute the rocchio algorithm optimization (YES/NO)? \n")
      if( (rocchio_choice=="YES" ) | (irevaluator_choice=="yes") ):
         print(" Executing Rocchio Algorithm")
         # The user chooses the X (e.g. X=20) first documents in the ranking and marks them as being relevant or non relevant according to the relevance assessments in MED.REL
         user_improvement = raw_input("Please, choose the X (e.g. X=20) first documents in the ranking and marks them as being relevant or non relevant according to the relevance assessments in MED.REL  \n")
         relevance_judgments = dict();
         for doc in ir.ranking_query[1][0:19]: # update the first 20 docs in the ranking 
             relevance_judgments[doc] = raw_input("Is relevant the document ID "  + str(doc[0]) +  " (Y/N)?")
         #5) According these relevance judgements, the system updates the original query based on Rocchio's formula.
    
         #6) The system launchs the new query and presents a new ranking.

         #7) A new P/R curve is generated and compared to the previous one. Is the system improving in precision and/or recall?

         #8) While not satisfied goto 4