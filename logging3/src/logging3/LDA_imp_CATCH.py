

import MySQLdb
import lda
import gensim
from nltk.tokenize import RegexpTokenizer
import re



import clean_fun


#==================================================================#
#  This file will be used to create LDA topics from the document
#==================================================================#


#Project
#"""
project= "tomcat_"
title = 'Apache Tomcat'
#"""
"""
project =  "cloudstack_"
title = 'CloudStack'
#"""

"""
project =  "hd_"
title = 'Hadoop'
#""

#"""
port=3306
user="root"
password="1234"
database="logging_level3"
catch_training_table = project+"catch_training3"
ratio_table= project+"catch_logging_ratio"
file_path="F:\\Research\\Logging3\\result\\"
"""

port=3307
user="sangeetal"
password="sangeetal"
database="logging_level3"
catch_training_table = project+"catch_training3"
ratio_table= project+"catch_logging_ratio"
#To save files on specified locations
file_path="E:\\Sangeeta\\Research\\Logging3\\result\\"
#"""


db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()

def build_and_print_LDA(docs_tokens):
       
    dictionary = gensim.corpora.Dictionary(docs_tokens)    
    corpus = [dictionary.doc2bow(doc_tokens) for doc_tokens in docs_tokens]
    
    #print " dict",  dictionary, corpus
    #model =  lda.LDA(n_topics =20, n_iter = 1500, random_state=1)
    #model.fit(corpus)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=500)
    
    data = ldamodel.print_topics(num_topics=20, num_words=10)
     
    i=0
    for d in data:
         print "Topic:", i, "=", d
         i=i+1    
        
     
def  create_lda_corpus(try_con_doc_tokens, is_catch_logged):
    str1 = "select try_con from " +  catch_training_table  +  "    where is_catch_logged="+ (str)(is_catch_logged)
    select_cursor.execute(str1)
    data1= select_cursor.fetchall()
    for d in data1:
        temp=d[0]
        #print " temp", temp
        clean_temp =  clean_fun.remove_special_char(temp)
        camel_temp  = clean_fun.camel_case_convert(clean_temp)
        lower_temp= camel_temp.lower()
        
        final_temp = lower_temp
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(final_temp)
        
        docs_tokens.append(tokens)
        #print "clean temp = ", tokens
        
    return docs_tokens    


docs_tokens= list()
try_con_doc_tokens = create_lda_corpus(docs_tokens, 1)        
build_and_print_LDA(docs_tokens) 


docs_tokens= list()
try_con_doc_tokens = create_lda_corpus(docs_tokens, 0)        
build_and_print_LDA(docs_tokens)      




#Tutorial: http://chrisstrelioff.ws/sandbox/2014/11/13/getting_started_with_latent_dirichlet_allocation_in_python.html

#2.   https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
