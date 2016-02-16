

import MySQLdb
import lda
import gensim
from nltk.tokenize import RegexpTokenizer
import re
from gensim.corpora.dictionary import Dictionary
import matplotlib.pyplot as plt
import numpy as np

import clean_fun
import util3




#============================================================================================================#
# There are some utility fucntion in the file clean_fun, please check if dont find the desired function here.
#=============================================================================================================#





def  plot_heat_map(lda_result, no_of_topics, plot_save_path):
#==== Now plot all the topics===#
    topic_labels = ['{}'.format(k) for k in range(no_of_topics)]
    #print topic_labels
    column_labels = list(topic_labels)
    
    i=0
    topic_tokens=list()
    topic_tokens_prob=list()
    
    for d in lda_result:
             print "Topic:", i, "=", d[1]
             topic_val=d[1]
             
             topic_tok= re.sub(r"[\*\.\+0-9]", " ", topic_val)
             topic_tok= re.sub(r" +", " ", topic_tok) 
             topic_tok= topic_tok.strip()       
             temp_tokens = topic_tok.split(' ')         
             
             topic_tok_prob= re.sub(r"[a-z\*\+]", " ", topic_val)
             topic_tok_prob= re.sub(r" +", " ", topic_tok_prob) 
             topic_tok_prob= topic_tok_prob.strip()
             temp_tokens_prob = topic_tok_prob.split(' ')  # not float its string
            
            
             topic_tokens.append(temp_tokens)  
             topic_tokens_prob.append(temp_tokens_prob)     
             
             i=i+1 
             
    #print topic_tokens  
    #print topic_tokens_prob
    
    #===Build Topic Dictinary======#
    
    topic_dictionary = gensim.corpora.Dictionary(topic_tokens)
    topic_term_prob_matrix = list()
    row_labels=list()
    
    for temp_key, temp_value in topic_dictionary.token2id.iteritems():
        
    
        temp_row = list()
        row_labels.append(temp_key)
        for i in range(no_of_topics):        
            
            temp_topic_token = topic_tokens[i] 
            temp_topic_key_prob = 0.0
            
            index = temp_topic_token.index(temp_key) if temp_key in temp_topic_token else -1
            if index!=-1:
                temp_topic_key_prob = (float)(topic_tokens_prob[i][index])
            
            temp_row.append(temp_topic_key_prob)
            print "Topic i=", i,  " key = ", temp_key, " index= ", index, " prob=",temp_topic_key_prob
            
            
        topic_term_prob_matrix.append(temp_row)    
    
    topic_term_prob_matrix = np.asanyarray(topic_term_prob_matrix)
    print  topic_term_prob_matrix,  topic_term_prob_matrix.shape[0], topic_term_prob_matrix.shape[1],  "row label = " ,len(row_labels), " row_label=",  row_labels
            
    
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(topic_term_prob_matrix, cmap=plt.cm.Blues)
    
    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(topic_term_prob_matrix.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(topic_term_prob_matrix.shape[0])+0.5, minor=False)
    
    
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    ax.set_xticklabels(column_labels, minor=False)
    ax.set_yticklabels(row_labels, minor=False)
    plt.savefig(plot_save_path)
   
    #plt.show()
    plt.close()
    