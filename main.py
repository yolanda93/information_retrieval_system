#!/usr/bin/python
import ir_system    
import rocchio_algorithm
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
    else: 
       only_query_id = raw_input("Write the ID of the query provided:\n")  # the user has provided a query or a text    
       return user_input, only_query_id

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
    elif irmodel_choice == 3:
       return ir_system.IR_Lda(corpus,query)
    elif irmodel_choice == 4:
       return ir_system.IR_Lda_Multicore(corpus,query)
    elif irmodel_choice == 5:
       return ir_system.IR_Lsi(corpus,query)
    elif irmodel_choice == 6:
       return ir_system.IR_Rp(corpus,query)
    elif irmodel_choice == 7:
       return ir_system.IR_LogEntropyModel(corpus,query)

#################################################################################
## @brief   execute_IRsystem_prompt
#  @details This method is used to interact with the user to execute their preferences  
#################################################################################  
def execute_IRsystem_prompt(corpus_text,query_text,only_query_id):

    print("\n The available models are: \n 0:Boolean\n 1:TF\n 2:TF-IDF\n 3:LDA\n 4:LDA Multicore\n 5:LSI\n 6:RP\n 7:LogEntropyModel\n \n")
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

       ir_evaluator.IREvaluator(relevances,ir.ranking_query,True,only_query_id)

    continue_choice = raw_input("Do you want to execute another IR model (YES/NO)? \n")

    if((continue_choice=="YES") | (continue_choice=="yes")):
         execute_IRsystem_prompt(corpus_text,query_text,only_query_id) # Call the method recursively
    else: 
         ir_evaluator.IREvaluator(relevances,ir.ranking_query,False,only_query_id)
    return ir
 
#################################################################################
## @brief   execute_Rocchio_prompt
#  @details This method is used to interact with the user to execute the rocchio 
#           algorithm evaluation  
#################################################################################               
def execute_Rocchio_prompt(query_text,corpus_text,ir,only_query_id):
     rocchio_choice = raw_input("Do you want to execute the rocchio algorithm optimization (YES/NO)? \n")
     if((rocchio_choice=="YES" ) | (rocchio_choice=="yes")):
         print("------------Executing Rocchio Algorithm------------")
         # The user chooses the X (e.g. X=20) first documents in the ranking and marks them as being relevant or non relevant according to the relevance assessments in MED.REL
         user_improvement = raw_input("Please, choose the X (e.g. X=20) first documents in the ranking and marks them as being relevant or non relevant according to the relevance assessments in MED.REL  \n")
         
         
         rankings = [list(i) for i in ir.ranking_query[1]] # convert to a list
         pos=0
         while pos < 20:
              answer = raw_input("Is relevant the document ID "  + str(rankings[pos][0]) +  " (Y/N)?")
              if (answer == 'y') or (answer == 'Y'):
                 rankings[pos][1] = 1      
              pos += 1          
         #5) According these relevance judgements, the system updates the original query based on Rocchio's formula.
         rocchio = rocchio_algorithm.RocchioAlgorithm(query_text,corpus_text,rankings,ir)
         #6) The system launchs the new query and presents a new ranking.
         #7) A new P/R curve is generated and compared to the previous one. 
         answer = 'y'
         while ((answer == 'y') or (answer == 'Y')):                
                 ir = execute_IRsystem_prompt(corpus_text,rocchio.new_query,only_query_id)
                 answer = raw_input("Do you want to execute again the rocchio optimization algorithm (Y/N)?") # desired recall and precision to be chosen by the user
     return 

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
      query_text, only_query_id=preprocess_userinput(query_input)

      ir = execute_IRsystem_prompt(corpus_text,query_text,only_query_id)
      rocchio = execute_Rocchio_prompt(query_text,corpus_text,ir,only_query_id)

