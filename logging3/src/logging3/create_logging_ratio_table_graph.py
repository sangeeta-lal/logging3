

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

del_str = " delete from "+insert_table
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


#=========================================#
# Plot Graphs
#=========================================#


#== Tomcat Graph ==#
#"""
plt.ylabel('ERCC Sum')
plt.xlabel('ERCC Range')
plt.title('Apache Tomcat')

ind = np.arange(1, 7 )   # the x locations for the groups
sum_exc_total_catch_ratio=[0.35, 0.09,0.14, 0.0, 0.42, 0]
sum_exc_total_catch_ratio=[35, 9, 14, 0, 42,0]
range_list=['0-5', '5-10', '10-15', '15-20','20-25', '>25']
labels = ['116', '1','1', '0','2','0']

print ind
width = 0.50     # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind,  sum_exc_total_catch_ratio, width, color='yellow', align = 'center')

ax = axes()
ylim(0,65)
plt.rcParams.update({'font.size': 25})
#plt.rcParams.update({'figure.autolayout': True})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')

rects = ax.patches

# Now make some labels
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom')

plt.savefig(file_path+"ercc\\tomcat_ercc.png", bbox_inches='tight')
#plt.show()
plt.close()

#"""

plt.ylabel('ERLC Sum')
plt.xlabel('ERCC Range')  #  It is ERCC range not ERLC hence correct.
plt.title('Apache Tomcat')

ind = np.arange(1, 7 )   # the x locations for the groups
sum_exc_total_log_ratio=[0.3797, 0.1601, 0.1409, 0, 0.319, 0]
sum_exc_total_log_ratio=[38, 16, 14, 0, 32, 0]
labels = ['116', '1','1', '0','2','0']

p1 = plt.bar(ind,  sum_exc_total_log_ratio, width, color='blue', align = 'center')

ax = axes()
ylim(0,65)
plt.rcParams.update({'font.size': 25})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')

#====New code====================================================##
rects = ax.patches

# Now make some labels
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom')
#===========================================================================================#

plt.savefig(file_path+"erlc\\tomcat_erlc.png", bbox_inches='tight')
#plt.show()
plt.close()

#=======================#
#  cloudstack 
#========================#

#"""
#plt.ylabel('ERCC')  #  Use Tomcat
plt.xlabel('ERCC Range')
plt.title('CloudStack')

ind = np.arange(1, 6) 
sum_exc_total_catch_ratio=[0.4354, 0.1273, 0.1276, 0.3115, 0.0]
sum_exc_total_catch_ratio=[43,      13,  13, 31, 0]
labels = ['158', '2','1', '2','0']
range_list=['0-5', '5-10', '10-15', '15-20','>20']

width = 0.50     # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind,  sum_exc_total_catch_ratio, width, color='yellow', align = 'center')
ax = axes()
ylim(0,70)
plt.rcParams.update({'font.size': 25})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')
rects = ax.patches

# Now make some labels
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom')


plt.savefig(file_path+"ercc\\cloudstack_ercc.png", bbox_inches='tight')
#plt.show()
plt.close()
#"""

#plt.ylabel('ERLC')  # Use Tomcat
plt.xlabel('ERCC Range')
plt.title('CloudStack')

sum_exc_total_log_ratio=[0.6097, 0, 0.3846, 0.0068, 0.0]
sum_exc_total_log_ratio=[61, 0, 38, 1, 0]
labels = ['158', '2','1', '2','0']


p1 = plt.bar(ind,  sum_exc_total_log_ratio, width, color='blue', align = 'center')

ax = axes()
ylim(0,70)
plt.rcParams.update({'font.size': 25})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')
#====New code====================================================##
rects = ax.patches
# Now make some labels
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom')
#===========================================================================================#


plt.savefig(file_path+"erlc\\cloudstack_erlc.png", bbox_inches='tight')
#plt.show()
plt.close()

#=====================================#
#  hadoop
#=====================================#

#== Tomcat Graph ==#
#"""
#plt.ylabel('ERCC')   # Use Tomcat
plt.xlabel('ERCC Range')
plt.title('Hadoop')

ind = np.arange(1, 8 )   # the x locations for the groups
sum_exc_total_catch_ratio=[0.4637, 0.0914, 0, 0.1598, 0, 0.286,0 ]
sum_exc_total_catch_ratio=[46, 9, 0, 16, 0, 29,0]
labels = ['262', '1','0', '1','0','1', '0']
range_list=['0-5', '5-10', '10-15', '15-20','20-25', '25-30','>30']

width = 0.5
p1 = plt.bar(ind,  sum_exc_total_catch_ratio, width, color='yellow', align = 'center')
ax = axes()
ylim(0,65)
plt.rcParams.update({'font.size': 25})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')
rects = ax.patches

# Now make some labels
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom')


plt.savefig(file_path+"ercc\\hd_ercc.png", bbox_inches='tight')
#plt.show()
plt.close()


#"""===================="""#
plt.close()
#plt.ylabel('ERLC')    #  Use Tomcat
plt.xlabel('ERCC Range')
plt.title('Hadoop')

sum_exc_total_log_ratio=[0.349 , 0.0813, 0, 0.1694, 0 , 0.4013,0 ]
sum_exc_total_log_ratio=[35, 8,0, 17, 0, 40,0]
labels = ['262', '1','0', '1','0','1', '0']

p1 = plt.bar(ind,  sum_exc_total_log_ratio, width, color='blue', align = 'center')
ax = axes()
ylim(0,65)
plt.rcParams.update({'font.size': 25})
#plt.rcParams.update({'figure.autolayout': True})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')

#====New code====================================================##
rects = ax.patches
# Now make some labels
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom')
#===========================================================================================#

plt.savefig(file_path+"erlc\\hd_erlc.png", bbox_inches='tight')
#plt.show()
