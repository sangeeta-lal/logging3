

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
file_path="F:\\Research\\Logging3\\result\\"
"""

port=3307
user="sangeetal"
password="sangeetal"
database="logging_level3"
catch_training_table = project+"catch_training3"
ratio_table =project+ "catch_logging_ratio"

#To save files on specified locations
file_path="E:\\Sangeeta\\Research\\Logging3\\result\\"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()
insert_cursor = db1.cursor()


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
        
    exc_total_catch_ratio       = round(exc_total_count*1.0/total_catch_count, 2)
    exc_log_catch_ratio         = round(exc_log_count*1.0/total_log_catch_count,2)
    logging_ratio              =  round(exc_log_count*1.0/exc_total_count, 2)
    non_logging_ratio          =  round(exc_non_log_count*1.0/exc_total_count, 2)
       
     
    print "log_count =", exc_log_count    

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
    

    