# Information Retrieval System 
   
The goal of this project is to implement a basic information retrieval system using Python, NLTK and GenSIM. 

To build this system, it is provided a plain text MED.ALL that contains many documents related to life sciences. Each document is composed by 2 fields (.I and .W). The field .I contains a numeric ID that identifies the document, while the field .W contains the text of the document.

For this system is created at least 3 different versions using different weights for building the vectors representing documents and queries.

The program supplies an entry point to enable the user to launch queries to the system.


Methods used to build the vectors:

(1) Standard Boolean Model

(2) TF weights

(3) TF-IDF weights

(4) Latent Semantic Indexing

(5) Latent Dirichlet Allocation


### Usage:

Script parameters:

* 


  
### Usage example:
```

```

![Alt text] (https://github.com/yolanda93/information_retrieval_system/blob/master/documents/images/Boolean%20Model.png "Usage example")

### Implementation

#### Standard Boolean Model
The Standard Boolean Model is most adopted information retrieval model and it is based on Boolean logic and classical set theory.

In order to implement this model it is used classical set theory. Therefore, the text is divided into phrases and then it is searched whithin each frase to find or operators.

**Algorithm steps**
  0. Check if there are or operators. if not goto 5.
  1. The query text is splitted into phrases based on "." tokens. These tokens are translated into an AND operator set
  2. For each phrase is searched the "or" token and splitted again. These tokens are translated into an OR operator set
  3. Look If there are AND_operator_sets (AND_operator_sets>1) to perform a query, goto 5. (The AND operator set is treated a single query in which all terms must appear in the text)
  4. For each element of the OR operator set goto 5 (the element is splitted using the OR as separator and each resulting phrase is executed as a single query)
  5. Execute the query and append documents to the final result if they dont exist already.
  

**Example queries**

   "blood or urinary steroids in human breast or prostatic neoplasms."
   
**Algorithm result**

 1. S; S =  " blood or urinary steroids in human breast or prostatic neoplasms."; lenght of AND_operator_set == 1
 2. S = AvBvC; A = "blood", B = "urinary steroids in human breast", C = "prostatic neoplasms."
 3.  AND_operator_set == 1
 4. Look for documents matches that dont exist already.
 5. Result = A_doc_matches + B_doc_matches  + C_doc_matches 


### Evaluating IR Systems

Evaluation the performance of the generated information retrieval models by comparing their average precision/recall curves for 30 different queries provided in the file MED.QRY. 

a third file called MED.REL is provided, which contains relevance assessments for each query in MED.QRY. Each line belonging to this file contains 4 colums, where only the first and the third are relevant for our purpose. The first colum identifies a query while the third column represents a document. Therefore the line:

1  0  13  1

Indicates that document with ID 13 is relevant to query 1 (the second and fourth column must be ignored). Another example:

2  0  296  1

indicates that document #296 is relevant to query #2.

For further information on how to create the average Precision/Recall curves please see the document Evaluation_Measures.pdf a third file called MED.REL is provided, which contains relevance assessments for each query in MED.QRY. Each line belonging to this file contains 4 colums, where only the first and the third are relevant for our purpose. The first colum identifies a query while the third column represents a document. Therefore the line:

1  0  13  1

Indicates that document with ID 13 is relevant to query 1 (the second and fourth column must be ignored). Another example:

2  0  296  1

indicates that document #296 is relevant to query #2.

For further information on how to create the average Precision/Recall curves please see the document Evaluation_Measures.pdf 

## Contact information
		
Yolanda de la Hoz Simón. yolanda93h@gmail.com
