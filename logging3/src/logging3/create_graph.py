
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import csv
import re
"""
#This file is used to craete graph for characterization study of logging 


"""

#Project
#"""
project= "tomcat_"
title = 'Apache Tomcat'
g1_y_upper = 30
g1_y_axis_label = "LOC   of   Try-Block"

g2_y_upper = 80
g2_y_axis_label = "Operator   Counts   of   Try-Block "

g3_y_upper = 30
g3_y_axis_label = "Method   Call   Counts   of   Try-Block "

file_sloc_y_upper = 400
file_sloc_y_axis_label= "File SLOC"

file_sloc_scatter_title = "Log Count"

#"""
"""
project =  "cloudstack_"
title = 'CloudStack'

g1_y_upper = 50
g1_y_axis_label = ""

g2_y_upper = 110
g2_y_axis_label = " "

g3_y_upper = 50
g3_y_axis_label = " "

file_sloc_y_upper = 400
file_sloc_y_axis_label= " "

file_sloc_scatter_title = " "
#"""

"""
project =  "hd_"
title = 'Hadoop'

g1_y_upper = 30
g1_y_axis_label = "" 

g2_y_upper =  80
g2_y_axis_label = " "

g3_y_upper = 30
g3_y_axis_label = " "

file_sloc_y_upper = 400
file_sloc_y_axis_label= " "

file_sloc_scatter_title = " "
#"""


#"""
port=3306
user="root"
password="1234"
database="logging_level3"
catch_training_table = project+"catch_training3"
ratio_table= project+"catch_logging_ratio"
file_sloc_table = project+"file_logging_density"
file_path="F:\\Research\\Logging3\\result\\"
"""

port=3307
user="sangeetal"
password="sangeetal"
database="logging_level3"
catch_training_table = project+"catch_training3"
ratio_table= project+"catch_logging_ratio"
#To save files on specified locations
file_sloc_table = project+"file_logging_density"
file_path="E:\\Sangeeta\\Research\\Logging3\\result\\"
#"""

db1= MySQLdb.connect(host="localhost",user=user, passwd=password, db=database, port=port)
select_cursor = db1.cursor()

#"""

def plot_var(y_lim_upper, title, y_axis_label, quartile_val):  

    plt.figure()
    box= plt.boxplot(data,0, 'bD', patch_artist=True, widths=0.35)
    colors = ['Yellow', 'Blue']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    
    for whisker in box['whiskers']:
        whisker.set(color='black', linewidth=1)
    for cap in box['caps']:
        cap.set(color='black', linewidth=1)
    for median in box['medians']:
        median.set(color='black', linewidth=1)
    
    ## change the style of fliers and their fill
    colors = ['Yellow', 'Blue']
    for flier, color1 in zip(box['fliers'], colors):
        flier.set(marker='o', color=color1, alpha=0.5)
        
    
    #==
    for line, temp_quartile in zip(box['medians'], quartile_val):
        # get position data for median line
        print "1=" ,line
        x,y = line.get_xydata()[1] # top of median line
       
        #extracting values of quartile
        q1= temp_quartile[0]
        med=temp_quartile[1]
        q3= temp_quartile[2]
        
        # overlay median value
        print "y=", y
        plt.rcParams.update({'font.size': 15})
        text(x+0.17, y-20, 'Q1= %.1f' % q1,
             horizontalalignment='center') # draw above, centered
        text(x+0.15, y, 'Med= %.1f' % med,
             horizontalalignment='center') # draw above, centered
        text(x+0.17, y+20, 'Q3= %.1f' % q3,
             horizontalalignment='center') # draw above, centered
    
    #print box.keys()    
    for line in box['boxes']:
        print line
     #   x, y = line.get_ydata() # bottom of left line
      #  text(x,y, '%.1f' % x,
      #       horizontalalignment='center', # centered
      #       verticalalignment='top')      # below
      #  x, y = line.get_xydata()[3] # bottom of right line
      #  text(x,y, '%.1f' % x,
      #       horizontalalignment='center', # centered
      #           verticalalignment='top')     

    #==
    
    ylim(0,y_lim_upper) 
    plt.rcParams.update({'font.size': 22})
    ax = axes()
    ax.set_xticklabels(['Logged ', 'Non Logged'])
    plt.suptitle(title)
    plt.ylabel(y_axis_label)


#=================Graph 1: Catch======================#
#@Compares LOC of logged and Non-Logged blocks
#==============================================#
"""
g1_log = "select try_loc from "+ catch_training_table+ " where is_catch_logged=1"
select_cursor.execute(g1_log)
g1_log_db = select_cursor.fetchall()
g1_data_log  = list()
#g1_data_log.append(2)
for d in g1_log_db:
    g1_data_log.append(d[0])

g1_non_log = "select try_loc from "+ catch_training_table+ " where is_catch_logged=0"
select_cursor.execute(g1_non_log)
g1_non_log_db = select_cursor.fetchall()
g1_data_non_log  = list()
for d in g1_non_log_db:
    g1_data_non_log.append(d[0])

print "length log = ", size(g1_data_log    ),"length  non= ", size(g1_data_non_log    )
data= [g1_data_log, g1_data_non_log]

log_quartile = list()
non_log_quartile = list()

q1_log= np.percentile(g1_data_log, 25)
med_log= np.median(g1_data_log)
q3_log = np.percentile(g1_data_log, 75)
log_quartile.append(q1_log)
log_quartile.append(med_log)
log_quartile.append(q3_log)

q1_non_log= np.percentile(g1_data_non_log, 25)
med_non_log = np.median(g1_data_non_log)
q3_non_log = np.percentile(g1_data_non_log, 75)
non_log_quartile.append(q1_non_log)
non_log_quartile.append(med_non_log)
non_log_quartile.append(q3_non_log)

quartile_val  = [log_quartile, non_log_quartile]
#==Call inbuilt function===#
plot_var(g1_y_upper, title, g1_y_axis_label, quartile_val)
#plt.show()
#plt.savefig(file_path+ "g1-try-loc\\"+project+"g1.png")

#==== Graph 2===================#
#@Compare operator count of logged and non logged catch blocks===#
#================================================================#
g2_log = "select operators_count_in_try from "+ catch_training_table+ " where  is_catch_logged=1"
select_cursor.execute(g2_log)
g2_log_db = select_cursor.fetchall()
g2_data_log  = list()
for d in g2_log_db:
    g2_data_log.append(d[0])


g2_non_log = "select  operators_count_in_try from "+ catch_training_table+ " where is_catch_logged=0"
select_cursor.execute(g2_non_log)
g2_non_log_db = select_cursor.fetchall()
g2_data_non_log  = list()
for d in g2_non_log_db:
    g2_data_non_log.append(d[0])

print "length log = ", size(g2_data_log ),"length  non= ", size(g2_data_non_log    )
data= [g2_data_log, g2_data_non_log]


log_quartile = list()
non_log_quartile = list()

q1_log= np.percentile(g2_data_log, 25)
med_log= np.median(g2_data_log)
q3_log = np.percentile(g2_data_log, 75)
log_quartile.append(q1_log)
log_quartile.append(med_log)
log_quartile.append(q3_log)

q1_non_log= np.percentile(g2_data_non_log, 25)
med_non_log = np.median(g2_data_non_log)
q3_non_log = np.percentile(g2_data_non_log, 75)
non_log_quartile.append(q1_non_log)
non_log_quartile.append(med_non_log)
non_log_quartile.append(q3_non_log)

quartile_val  = [log_quartile, non_log_quartile]


plot_var(g2_y_upper, title, g2_y_axis_label, quartile_val)
#plt.show()
#plt.savefig(file_path+ "g2-try-op\\"+project+"g2.png")



#==== Graph 3==================#
#@Method Call count of logged and non logged catch blocks===#
#================================================================#
g3_log = "select method_call_count_try from "+ catch_training_table+ " where  is_catch_logged=1"
select_cursor.execute(g3_log)
g3_log_db = select_cursor.fetchall()
g3_data_log  = list()
for d in g3_log_db:
    g3_data_log.append(d[0])


g3_non_log = "select  method_call_count_try from "+ catch_training_table+ " where is_catch_logged=0"
select_cursor.execute(g3_non_log)
g3_non_log_db = select_cursor.fetchall()
g3_data_non_log  = list()
for d in g3_non_log_db:
    g3_data_non_log.append(d[0])

print "length log = ", size(g3_data_log ),"length  non= ", size(g3_data_non_log    )
data= [g3_data_log, g3_data_non_log]

log_quartile = list()
non_log_quartile = list()

q1_log= np.percentile(g3_data_log, 25)
med_log= np.median(g3_data_log)
q3_log = np.percentile(g3_data_log, 75)
log_quartile.append(q1_log)
log_quartile.append(med_log)
log_quartile.append(q3_log)

q1_non_log= np.percentile(g3_data_non_log, 25)
med_non_log = np.median(g3_data_non_log)
q3_non_log = np.percentile(g3_data_non_log, 75)
non_log_quartile.append(q1_non_log)
non_log_quartile.append(med_non_log)
non_log_quartile.append(q3_non_log)

quartile_val  = [log_quartile, non_log_quartile]

plot_var(g3_y_upper, title, g3_y_axis_label, quartile_val)
#plt.show()
#plt.savefig(file_path+ "g3-try-method-call\\"+project+"g3.png")




#===========================================================
# @Graph4: Exception Type Vs. Positive or Negative Logging ratio
#==============================================================
pos_count_threshold = 5
neg_count_threshold = 10

pos_ratio_threshold = 60.0
neg_ratio_threshold = 80.0
exc_count_above_threshold= list()
exc_pos_ratio_above_threshold =list()
exc_neg_ratio_above_threshold =list()

g4_str = "select distinct catch_exc  from "+ catch_training_table  
#print " g4_str=",g4_str
select_cursor.execute(g4_str)
g4_db = select_cursor.fetchall()
unique_exc=list()
for d in g4_db:
    unique_exc.append(d[0])

#print "len=", size(unique_exc)    
for temp_exc in unique_exc:
    #print temp_exc           
    exc_str = " select count(*)   from " + catch_training_table + " where catch_exc = '"+temp_exc+"'"
    select_cursor.execute(exc_str)
    data1 =  select_cursor.fetchall()
    
    total_count= 0
    for d in data1:
        total_count = d[0]
        
    if total_count >= pos_count_threshold:
       
        pos_str = "select count(*)  from   " + catch_training_table +  "  where catch_exc = '"+ temp_exc+ "'  and is_catch_logged = 1"
        select_cursor.execute(pos_str)
        data2 = select_cursor.fetchall()
    
        pos_count = 0 
        for d in data2:  
            pos_count =d[0]     
        
            
    if total_count >= neg_count_threshold:    
        neg_str = "select count(*)  from   " + catch_training_table +  "  where catch_exc = '"+ temp_exc+ "'  and is_catch_logged = 0"
        select_cursor.execute(neg_str)
        data2 = select_cursor.fetchall()
    
        neg_count = 0 
        for d in data2:  
            neg_count =d[0]  
             
            
        pos_ratio = ((pos_count*100.0)/total_count)
        neg_ratio = ((neg_count*100.0)/total_count)
        
        if temp_exc!='Exception':
            temp_exc= re.sub('Exception$','',temp_exc)
        
        temp_obj_list =list()
        if pos_ratio >= pos_ratio_threshold:
            temp_obj_list.append(temp_exc)
            temp_obj_list.append(pos_ratio)
            
            exc_pos_ratio_above_threshold.append(temp_obj_list)  
        
        temp_obj_list =list()
        if neg_ratio >= neg_ratio_threshold:
            temp_obj_list.append(temp_exc)
            temp_obj_list.append(neg_ratio)
            
            exc_neg_ratio_above_threshold.append(temp_obj_list)  


print " pos ratio = ", exc_pos_ratio_above_threshold
print " neg ratio = ",exc_neg_ratio_above_threshold

#==pos Plot===#


ratio_list=list()
for temp_ratio in  exc_pos_ratio_above_threshold:
    ratio_list.append(int(temp_ratio[1]))
exc_list=list()  
for temp_exc in  exc_pos_ratio_above_threshold:
    exc_list.append(temp_exc[0])

#==pos ratio plot===#
print ratio_list
plt.ylabel('Logged Ratio')
plt.title(title)

ind = np.arange(1, size(ratio_list)+1 )   # the x locations for the groups
print ind
width = 0.50     # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind, ratio_list, width, color='yellow', align = 'center')

ax = axes()
ylim(0,100)
plt.rcParams.update({'font.size': 25})
#plt.rcParams.update({'figure.autolayout': True})
plt.tight_layout()
plt.xticks(ind, exc_list, rotation=290, fontsize=20,  ha='left')

#plt.show()
plt.savefig(file_path+"g-exc-ratio\\"+project+"pos_ratio.png",bbox_inches='tight')


#=== neg plot===#

ratio_list=list()
for temp_ratio in  exc_neg_ratio_above_threshold:
    ratio_list.append(int(temp_ratio[1]))
exc_list=list()  
for temp_exc in  exc_neg_ratio_above_threshold:
    exc_list.append(temp_exc[0])

#===neg ratio plot===#
plt.clf()# clear earlier plot
print ratio_list
plt.ylabel('Non Logged Ratio')
plt.title(title)

ind = np.arange(1, size(ratio_list)+1 )   # the x locations for the groups
print ind
width = 0.50     # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind, ratio_list, width, color='blue', align = 'center')

ax = axes()
ylim(0,100)
plt.rcParams.update({'font.size': 25})
#plt.rcParams.update({'figure.autolayout': True})
plt.tight_layout()
plt.xticks(ind, exc_list, rotation=290, fontsize=20,  ha='left')

#plt.show()
plt.savefig(file_path+"g-exc-ratio\\"+project+"neg_ratio.png",bbox_inches='tight')


#================================================================================================#
#G5: Print logging ratio of 20 most popular exceptions.
#=================================================================================================#

str1= "select catch_exc, count(*)  from  "+  catch_training_table + "  group by catch_exc  order by count(*)  desc limit 0, 20" 
select_cursor.execute(str1)
data =  select_cursor.fetchall()
exc_info = list()
for d in data:
    print  d[0], d[1]
    
    exc= d[0]
    exc_total_count = d[1]    
    str_nest = "select count(*)  from "+  catch_training_table + "  where catch_exc = '"+ exc+ "' and  is_catch_logged = 1"    
    select_cursor.execute(str_nest)
    data_nest = select_cursor.fetchall()
    
    exc_log_count = 0
    for d_n in data_nest:
        exc_log_count = d_n[0]
        
    print "log_count =", exc_log_count    

    temp = list()
    temp.append(exc)
    temp.append(exc_total_count)
    temp.append(exc_log_count)
    temp.append(exc_total_count - exc_log_count)
    
    exc_info.append(temp)

print " list", exc_info  


with open(file_path+"\\"+project+"top-20.csv", 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Exception Type ']+ ['Total Count','Log Count','Non Log Count', 'Logged Ratio', 'Non-Logged Ratio'])
    
    #====================Graph5==============================#
    #==================heatMap================================#
   
    for row in exc_info:
        
         spamwriter.writerow([row[0]+ ","+(str)(row[1])+","+(str)(row[2])+","+(str)(row[3] ) +","+(str)((float)(((row[2]*100.0)/row[1]*1.0)))+"," +(str)((float)((((row[3]*100.0)/row[1]*1.0))))])
        



#================================================
# G6 : PIE Chart of 20 most popular exceptions
#===============================================
total_count = 0.0
other_count = 0.0
top_20_count = 0.0


str_total =  "select count(*)   from  "+ catch_training_table 
select_cursor.execute(str_total)
data1 =  select_cursor.fetchall()
for d in data1:
    total_count = (float)(d[0])

str_top_20= "select sum(exc_total_count)  from ( select exc_total_count  from "+ ratio_table+ "    order by exc_total_count desc limit 0, 20) as  temp_table"     
select_cursor.execute(str_top_20)
data1 =  select_cursor.fetchall()
for d in data1:
    top_20_count =(float)( d[0])

other_count =  total_count - top_20_count

print other_count, total_count, top_20_count
other_percent =  ((other_count*100.0 )/total_count)
top_20_percent = ( (top_20_count*100.0)/total_count)  
# make a square figure and axes
plt.close()
plt.figure(1, figsize=(6,6))
ax = axes([0.1, 0.1, 0.8, 0.8])

# The slices will be ordered and plotted counter-clockwise.
labels = 'Others', 'Top-20 '
fracs = [other_percent, top_20_percent]
explode=(0, 0.08)

cs = ['blue', 'yellow']
plt.pie(fracs, colors = cs, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90)
              
plt.savefig(file_path+ "top_20_pie\\"+project+"pie.png")

#plt.show()
plt.close()


#====================================================================================
# G7: It is about co-existence of logged and non-logged catch blocks together
#=====================================================================================  


unique_try_blocks = 0
mix_try_blocks = 0
try_blocks_more_than_1_catch = 0
 
str1= " select   count( distinct try_id ) from "+ catch_training_table  
print "str1 = ", str1  
select_cursor.execute(str1)
data1 = select_cursor.fetchall()
for d in data1:
    unique_try_blocks = d[0]
    
    

str_more_than_1_catch  = "create table temp (select    try_id, count(*)  from  " +  catch_training_table  + "  group by try_id    having count(*) >1 )"
print "str more than 1 catch=", str_more_than_1_catch
select_cursor.execute(str_more_than_1_catch)
db1.commit()# create the temp table

str_temp= "select count(*) from temp"
select_cursor.execute(str_temp)
data3 = select_cursor.fetchall()
for d in data3:
    try_blocks_more_than_1_catch =  d[0]
 
drop_temp= "drop table temp"
select_cursor.execute(drop_temp)  
db1.commit()# ==delete the table

str_mix_logged_non_logged = "select count( distinct try_id)  from  "+ catch_training_table+ " where is_catch_logged=0 and try_id in (select   distinct try_id  from  "+ catch_training_table+ " where is_catch_logged=1) "    
select_cursor.execute(str_mix_logged_non_logged)
data2 =  select_cursor.fetchall()

for d in data2:
    mix_try_blocks = d[0]
    

print " Unique Try block = ", unique_try_blocks,  "  mix try blocks=", mix_try_blocks, "  try blocks more than 1 catch block=",  try_blocks_more_than_1_catch    
  
  
#=================================================================================================
#  G8: ERCC nad ERLC graph are present in this file. ==> create_logging_ratio_table_graph.py
#=================================================================================================  


#=================================================================================================#
#  G9: Logging ratio distribution
#==================================================================================================#
total_exc_types=0.0
between_0_10_p=0.0
between_10_20_p=0.0
between_20_30_p=0.0
between_30_10_p=0.0
between_40_10_p=0.0
between_50_10_p=0.0
between_60_10_p=0.0
between_70_10_p=0.0
between_80_10_p=0.0
between_90_10_p=0.0


logging_ratio= list()
logging_ratio_count = list()

str1= "select count(*)  from (select   distinct catch_exc   from  " +   catch_training_table  +"  ) as abb  "
select_cursor.execute(str1)
data1=select_cursor.fetchall()
for d in data1:
    total_exc_types=d[0]*1.0  #  comvert to float
print  total_exc_types

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0  and logging_ratio<0.10 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_0_10_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.10  and logging_ratio<0.20 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_10_20_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.20  and logging_ratio<0.30 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_20_30_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.30  and logging_ratio<0.40 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_30_40_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.40  and logging_ratio<0.50 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_40_50_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.50  and logging_ratio<0.60 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_50_60_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])
 

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.60  and logging_ratio<0.70 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_60_70_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.70  and logging_ratio<0.80 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_70_80_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])

str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.80  and logging_ratio<0.90 "
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_80_90_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])
    
str1 = " select  count(*)  from "  + ratio_table +"  where logging_ratio >=0.90"
#print "str1 = ", str1
select_cursor.execute(str1)
data1= select_cursor.fetchall()
for d in data1:
    temp= (d[0]*1.0)
    between_90_100_p=round(temp/total_exc_types,2)*100
    logging_ratio_count.append(d[0])


logging_ratio.append((int)( between_0_10_p))
logging_ratio.append((int)(  between_10_20_p))
logging_ratio.append((int)(  between_20_30_p))
logging_ratio.append((int)(  between_30_40_p))
logging_ratio.append((int)( between_40_50_p))
logging_ratio.append((int)(  between_50_60_p))
logging_ratio.append((int)(  between_60_70_p))
logging_ratio.append((int)(  between_70_80_p))
logging_ratio.append((int)(  between_80_90_p))
logging_ratio.append((int)(  between_90_100_p))

print logging_ratio
print "logging_ratio_count=0"
#========================================#    
#=== create hostogram fo the same========# 
if project=='tomcat_':
    plt.ylabel('% of Exception Types')
else:
    plt.ylabel('')    

plt.xlabel('Logging Ratio')
plt.title(title)

ind = np.arange(1, 11 )   # the x locations for the groups
range_list=['<10', '10-20', '20-30', '30-40','40-50', '50-60', '60-70', '70-80', '80-90', '>=90']



width = 0.50     # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind,  logging_ratio, width, color='yellow', align = 'center')

ax = axes()
ylim(0,100)
plt.rcParams.update({'font.size': 20})
#plt.rcParams.update({'figure.autolayout': True})
plt.tight_layout()
plt.xticks(ind, range_list, rotation=290, fontsize=20,  ha='left')

rects = ax.patches

# Now make some labels
#
for rect, label in zip(rects, logging_ratio_count):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 2, label, ha='center', va='bottom') 

plt.savefig(file_path+"logging_ratio\\"+project+"logging_ratio.png", bbox_inches='tight')
plt.show()
plt.close()

"""



#========================================================================#
#  G10: This graph makes box-plots for the sloc of the files.            #
#========================================================================#
avg_sloc_non_logged =  0.0
avg_sloc_logged = 0.0

str_sloc  = "select avg(file_sloc)  from  "+ file_sloc_table + " where is_logged = 1"
select_cursor.execute(str_sloc)
data =  select_cursor.fetchall()
for d in data:
    avg_sloc_logged = d[0]



str_sloc  = "select avg(file_sloc)  from  "+ file_sloc_table  +"  where is_logged = 0"
select_cursor.execute(str_sloc)
data =  select_cursor.fetchall()
for d in data:
    avg_sloc_non_logged = d[0]

print "avg total sloc= ", avg_sloc_logged, "  avg sloc logged=", avg_sloc_non_logged


#===Make the Box-Plot===================================================#
file_sloc_log = "select file_sloc from "+ file_sloc_table+ " where is_logged=1"
select_cursor.execute(file_sloc_log)
file_sloc_log_db = select_cursor.fetchall()
file_sloc_data_log  = list()
#file_sloc_data_log.append(2)
for d in file_sloc_log_db:
    file_sloc_data_log.append(d[0])

file_sloc_non_log = "select file_sloc from "+ file_sloc_table+ " where is_logged=0"
select_cursor.execute(file_sloc_non_log)
file_sloc_non_log_db = select_cursor.fetchall()
file_sloc_data_non_log  = list()
for d in file_sloc_non_log_db:
    file_sloc_data_non_log.append(d[0])

print "length sloc log = ", size(file_sloc_data_log    ),"length  sloc non logged= ", size(file_sloc_data_non_log    )
data= [file_sloc_data_log, file_sloc_data_non_log]

log_quartile = list()
non_log_quartile = list()

q1_log= np.percentile(file_sloc_data_log, 25)
med_log= np.median(file_sloc_data_log)
q3_log = np.percentile(file_sloc_data_log, 75)
log_quartile.append(q1_log)
log_quartile.append(med_log)
log_quartile.append(q3_log)

q1_non_log= np.percentile(file_sloc_data_non_log, 25)
med_non_log = np.median(file_sloc_data_non_log)
q3_non_log = np.percentile(file_sloc_data_non_log, 75)
non_log_quartile.append(q1_non_log)
non_log_quartile.append(med_non_log)
non_log_quartile.append(q3_non_log)

quartile_val  = [log_quartile, non_log_quartile]
#==Call inbuilt function===#
plot_var(file_sloc_y_upper, title, file_sloc_y_axis_label, quartile_val)
#plt.show()
plt.savefig(file_path+ "file_sloc\\"+project+"file_sloc.png")

plt.close()

#==========================================================#
#========Make Scatter Plot of File SLOC Vs. Log Count for logged files======#
sloc_vs_log_count = "select file_sloc, log_count from "+ file_sloc_table+ " where is_logged=1"
select_cursor.execute(sloc_vs_log_count)
sloc_log_count_db = select_cursor.fetchall()

file_sloc_log  = list()
file_log_count = list()

#file_sloc_data_log.append(2)
for d in sloc_log_count_db:
    file_sloc_log.append(d[0])
    file_log_count.append(d[1])
    
plt.figure()

z = np.polyfit(file_sloc_log,file_log_count,1)
p = np.poly1d(z)

#plt.scatter(file_sloc_log, file_log_count)
plt.plot(file_sloc_log, file_log_count, 'o', file_sloc_log, p(file_sloc_log),'r--')
ax = plt.subplot()
max_sloc =max( file_sloc_log)
max_log_count = max(file_log_count)
ax.set_xlim([0, max_sloc + 1000])
ax.set_ylim([0, max_log_count + 10])
plt.suptitle(title)
plt.xlabel("File SLOC")
plt.ylabel(file_sloc_scatter_title)
plt.rcParams.update({'font.size': 22})
#plt.show()    
plt.savefig(file_path+ "file_sloc_scatter\\"+project+"file_sloc_scatter_logged.png", bbox_inches='tight')
plt.close()


#========================================================================#
#========Make Scatter Plot of File SLOC Vs. Log Count for all files======#
sloc_vs_log_count = "select file_sloc, log_count from "+ file_sloc_table
select_cursor.execute(sloc_vs_log_count)
sloc_log_count_db = select_cursor.fetchall()

file_sloc_all  = list()
file_log_count = list()

#file_sloc_data_log.append(2)
for d in sloc_log_count_db:
    file_sloc_all.append(d[0])
    file_log_count.append(d[1])
    
plt.figure()

z = np.polyfit(file_sloc_all,file_log_count,1)
p = np.poly1d(z)

#plt.scatter(file_sloc_all, file_log_count, c='yellow', file_sloc_all, p(file_sloc_all),'r--')
plt.plot(file_sloc_all, file_log_count, 'yo', file_sloc_all, p(file_sloc_all),'r--')

ax = plt.subplot()
max_sloc =max( file_sloc_all)
print " max-sloc=", max_sloc
max_log_count = max(file_log_count)
ax.set_xlim([0, max_sloc + 1000])
ax.set_ylim([0, max_log_count + 10])
plt.suptitle(title)
plt.xlabel("File SLOC")
plt.ylabel(file_sloc_scatter_title)
plt.rcParams.update({'font.size': 22})
#plt.show()    
plt.savefig(file_path+ "file_sloc_scatter\\"+project+"file_sloc_scatter_all.png", bbox_inches='tight')
plt.close()
