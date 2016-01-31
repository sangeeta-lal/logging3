

import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import csv
import re
import math

#==================================================#
#@Uses: Logging frequency Vs. Exception frequency 
#==================================================#


"""==========================================================================================================
#This file is used to create graph for characterization study of logging  ratio with respect to exception ratio

============================================================================================================="""

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
ratio_table =project+ "catch_logging_ratio"
insert_table=project+"exc_count_vs_log_ratio_graph"
file_path="F:\\Research\\Logging3\\result\\"
"""

port=3307
user="sangeetal"
password="sangeetal"
database="logging_level3"
catch_training_table = project+"catch_training3"
ratio_table =project+ "catch_logging_ratio"
insert_table=project+"exc_count_vs_log_ratio_graph"
#To save files on specified locations
file_path="E:\\Sangeeta\\Research\\Logging3\\result\\"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
insert_cursor = db1.cursor()

#======================================
#  Delete from ratio table
#======================================

del_str = " delete from " + ratio_table
select_cursor.execute(del_str)
db1.commit()
#=======================================

total_catch_count = 0
total_log_catch_count = 0
exc_info = list()

str1 = "select  count(*)  from  "+  catch_training_table
select_cursor.execute(str1)
data1 = select_cursor.fetchall()
for d in data1:    
    total_catch_count= d[0]
       

str1 = "select  count(*)  from  "+  catch_training_table +"   where is_catch_logged = 1"
select_cursor.execute(str1)
data1 = select_cursor.fetchall()
for d in data1:    
    total_log_catch_count= d[0]    
    

str1 = "select catch_exc, count(*)  from  "+  catch_training_table +"   group by catch_exc"
select_cursor.execute(str1)
data1 = select_cursor.fetchall()

for d in data1:
    
    exc= d[0]
    exc_total_count = d[1]    
    str_nest = "select count(*)  from "+  catch_training_table + "  where catch_exc = '"+ exc+ "' and  is_catch_logged = 1"    
    select_cursor.execute(str_nest)
    data_nest = select_cursor.fetchall()
    
    exc_log_count = 0
    exc_non_log_count=0
    for d_n in data_nest:
        exc_log_count = d_n[0]
        exc_non_log_count= exc_total_count - exc_log_count
        
    exc_total_catch_ratio       = round(exc_total_count*1.0/total_catch_count, 4)
    exc_log_catch_ratio         = round(exc_log_count*1.0/total_log_catch_count,4)
    logging_ratio              =  round(exc_log_count*1.0/exc_total_count, 4)
    non_logging_ratio          =  round(exc_non_log_count*1.0/exc_total_count, 4)
       
     
    print "log_count =", exc_log_count  ,    exc_log_catch_ratio  

    temp = list()
    temp.append(exc)
    temp.append(exc_total_count)
    temp.append(exc_total_catch_ratio)
    temp.append(exc_log_count)
    temp.append(exc_log_catch_ratio)
    temp.append(logging_ratio)
    temp.append(non_logging_ratio)
    temp.append(total_catch_count)
    temp.append(total_log_catch_count)
    exc_info.append(temp)
    
    
    #==Insret all the information====#
    
    insert_str = " insert into " +  ratio_table +  "  values('"+ exc+"',"+ (str)(exc_total_count) +","+ (str)(exc_total_catch_ratio)+","+(str)(exc_log_count)+","+(str)(exc_log_catch_ratio)+","+\
                 (str)(logging_ratio)+","+(str)(non_logging_ratio)+","+(str)(total_catch_count)+","+(str)(total_log_catch_count)+")"
    
    insert_cursor.execute(insert_str)    
    db1.commit()             
                 
    print "temp", temp
    


#===========================================================#
#G7:
#============================================================#

ratio_details=list()
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio <=0.05 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0-0.05'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0        
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.05  and exc_total_catch_ratio<=0.10 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.05-0.10'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)  
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.10  and exc_total_catch_ratio<=0.15 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.10-0.15'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.15  and exc_total_catch_ratio<=0.20 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.15-0.20'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.20  and exc_total_catch_ratio<=0.25 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.20-0.25'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"   
    print " insert", insert_str 
    insert_cursor.execute(insert_str)          
     
      
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.25  and exc_total_catch_ratio<=0.30 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.25-0.30'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    

    
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.30  and exc_total_catch_ratio<=0.35 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.30-0.35'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.35  and exc_total_catch_ratio<=0.40 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.35-0.40'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0    
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.40  and exc_total_catch_ratio<=0.45 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.40-0.45'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0   
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
    
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.45  and exc_total_catch_ratio<=0.50 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '0.45-0.50'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0   
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)                     
          
          
str1 = "  select count(catch_exc), sum(  exc_total_catch_ratio) ,sum(exc_log_catch_ratio)   from    "+  ratio_table  + " where  exc_total_catch_ratio >0.50 "
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    range= '> 0.50'
    diff_exc_count= d[0]
    sum_exc_total_catch_ratio= d[1]
    sum_exc_log_catch_ratio =d[2]
    
    if diff_exc_count is None:
        diff_exc_count = 0
    if sum_exc_total_catch_ratio is None:
        sum_exc_total_catch_ratio = 0.0
    if sum_exc_log_catch_ratio is None:
        sum_exc_log_catch_ratio = 0.0   
    
    insert_str= "insert  into "+ insert_table + "   values('"+range+"',"+ (str) (diff_exc_count) +","+ (str) (sum_exc_total_catch_ratio)+","+  (str)(sum_exc_log_catch_ratio)+")"    
    insert_cursor.execute(insert_str)
    
db1.commit()              