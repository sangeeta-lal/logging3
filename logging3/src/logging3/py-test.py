

import MySQLdb
import lda
import gensim
from nltk.tokenize import RegexpTokenizer
import re
from gensim.corpora.dictionary import Dictionary



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
#"""

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

def build_and_print_LDA(docs_tokens, no_of_topics, no_of_words, low_lim_val):
           
    dictionary = gensim.corpora.Dictionary(docs_tokens)    
    print dictionary , " low lim", low_lim_val
    
    dictionary.filter_extremes(low_lim_val, above_lim_val)
    dictionary.compactify()
    
    print "after removing=", dictionary
    
    corpus = [dictionary.doc2bow(doc_tokens) for doc_tokens in docs_tokens]
    
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=no_of_topics, id2word = dictionary, passes=no_lda_iterations)    
    lda_res  = ldamodel.print_topics(num_topics=no_of_topics, num_words=no_of_words)
    
 
    return lda_res
    
        
     
def  create_lda_corpus(try_con_doc_tokens, is_catch_logged, low_lim):
   # str1 = "select try_con from " +  catch_training_table  +  "    where is_catch_logged="+ (str)(is_catch_logged)
   # select_cursor.execute(str1)
   # data1= select_cursor.fetchall()
    
   
    data1= ['I amSangeeta', 'Hello i', 'i am san', ' this teaching nl i', 'this nl teach i', 'i nl teac', 'i the sangeeta', 'i the see', 'i the rem', 'i pl', 'see', 'i jjk', 'i jjjj', ' i hhhh']
    low_lim_val= (len(data1)*low_lim)/100.0
    print "low lim val:(=", low_lim_val, "  len data1", len(data1)

    for d in data1:
        temp=d   ##Specialfile
        print " temp", temp
        clean_temp   =  clean_fun.remove_special_char(temp)
        camel_temp   =  clean_fun.camel_case_convert(clean_temp)
        lower_temp   =  camel_temp.lower()
        stop_temp    =  clean_fun.remove_stop_words (lower_temp)
      
        stemmed_temp =  clean_fun.stem_it(stop_temp)
         
        final_temp = stemmed_temp
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(final_temp)
        
        docs_tokens.append(tokens)
        print "clean temp = ", final_temp
        
    return docs_tokens, low_lim_val  



def write_in_file(lda_results, file_handle, no_of_topics, no_of_words, lda_iterations):
    file_handle.write("no_of_topics=" +(str)(no_of_topics)+"\n")
    file_handle.write("no_of_words=" +(str)(no_of_words)+"\n")
    file_handle.write("no_of_lda_iteration=" +(str)(lda_iterations)+"\n")
    i=0
    
    for d in lda_results:
         print "Topic:", i, "=", d
         file_handle.write("Topic "+ (str)(i)+ "="+(str)(d)+"\n")
         i=i+1  

#==============================================#
#==============================================#
no_of_topics = 20
no_of_words = 10
no_lda_iterations = 10
docs_tokens= list()
try_con_logged_doc_tokens  = list()
try_con_non_logged_doc_tokens = list()
#=====Filter words=============================#
#  filter words which occur in less than equal to 2% or geater than 80% of the docs
low_lim= 2 # Remove tokens which occur in less than 2% of documents

low_lim_val= 0   #  compute from create_lda_corpus function uses low_lim
above_lim_val=0.80

#================================================#

print " Topics from Try-Block of Logged Catch Blocks:"
print  "==========================================="
logged_file_path = file_path+"lda\\" +project + "lda_"+(str)(no_of_topics)+"_"+(str)(no_of_words)+"try_logged.txt"
file_handle =  open(logged_file_path, 'w')

try_con_logged_doc_tokens, low_lim_val = create_lda_corpus(docs_tokens, 1, low_lim)        
lda_result = build_and_print_LDA(docs_tokens, no_of_topics, no_of_words, low_lim_val) 
write_in_file(lda_result, file_handle, no_of_topics, no_of_words, no_lda_iterations)
file_handle.close()


docs_tokens = list()  # reset this
print " Topics from Try-Block of non Logged Catch Blocks:"
print  "==========================================="
non_logged_file_path = file_path+"lda\\" +project + "lda_"+(str)(no_of_topics)+"_"+(str)(no_of_words)+"try_non_logged.txt"
file_handle =  open(non_logged_file_path, 'w')


try_con_non_logged_doc_tokens, low_lim_val = create_lda_corpus(docs_tokens, 1, low_lim)        
lda_result = build_and_print_LDA(docs_tokens, no_of_topics, no_of_words, low_lim_val) 
write_in_file(lda_result, file_handle, no_of_topics, no_of_words, no_lda_iterations)
file_handle.close()
"""

##===== Logged catch block=============##
non_logged_file_path = file_path+"lda\\" +project + "lda_"+(str)(no_of_topics)+"_"+(str)(no_of_words)+"try_non_logged.txt"
file_handle =  open(non_logged_file_path, 'w')

print " Topics from Try-Block of Non-Logged Catch Blocks:"
print  "==========================================="
try_con_doc_tokens, low_lim_val = create_lda_corpus(docs_tokens, 0, low_lim_val)        
lda_result = build_and_print_LDA(docs_tokens, no_of_topics, no_of_words, low_lim_val) 
write_in_file(lda_result, file_handle, no_of_topics, no_of_words, no_lda_iterations)
file_handle.close()

"""

#http://radimrehurek.com/topic_modeling_tutorial/2%20-%20Topic%20Modeling.html   (Removing frequent and nin frequent words)


#Tutorial: http://chrisstrelioff.ws/sandbox/2014/11/13/getting_started_with_latent_dirichlet_allocation_in_python.html

#2.   https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
