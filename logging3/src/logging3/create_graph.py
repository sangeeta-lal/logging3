
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
"""
#This file is used to craete graph for characterization study of logging 

"""

#Project
#"""
project= "tomcat_"
title = 'Apache Tomcat'
g1_y_upper = 30
g1_y_axis_label = "LOC   of   Try-Block"

g2_y_upper = 200
g2_y_axis_label = "Operator   Counts   of   Try-Block "

g3_y_upper = 50
g3_y_axis_label = "Method   Call   Counts   of   Try-Block "

"""
project =  "cloudstack_"
graph_title = 'CloudStack'

g1_y_upper = 200
g1_y_axis_label = "LOC   of   Try-Block"

g2_y_upper = 200
g2_y_axis_label = "Operator   Counts   of   Try-Block "

g3_y_upper = 200
g3_y_axis_label = "Method   Call   Counts   of   Try-Block "
#"""

"""
project =  "hd_"
graph_title = 'Hadoop'

g1_y_upper = 
g1_y_axis_label = "LOC   of   Try-Block"

g2_y_upper = 
g2_y_axis_label = "Operator   Counts   of   Try-Block "

g3_y_upper = 
g3_y_axis_label = "Method   Call   Counts   of   Try-Block "
#"""

"""
#project = "jboss_"
#"""


#"""
port=3306
user="root"
password="1234"
database="logging_level3"
catch_training_table = project+"catch_training3"
"""
port=3307
user="sangeetal"
password="sangeetal"
database="logging_level3"
catch_training_table = project+"catch_training3"

#To save files on specified locations
file_path="D:\\Research\\Logging3\\result\\graph\\"
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
        text(x+0.17, y-1.2, 'Q1= %.1f' % q1,
             horizontalalignment='center') # draw above, centered
        text(x+0.15, y, 'Med= %.1f' % med,
             horizontalalignment='center') # draw above, centered
        text(x+0.17, y+1.2, 'Q3= %.1f' % q3,
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
plt.show()


#==== Graph 2==================#
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

plot_var(g2_y_upper, title, g2_y_axis_label)
plt.show()



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

plot_var(g3_y_upper, title, g3_y_axis_label)
plt.show()

#"""

"""===========================================================
# @Graph4: Exception Type Vs. Positive or Negative Logging ratio
=============================================================="""
total_count_threshold = 5
pos_ratio_threshold = 60.0
neg_ratio_threshold = 100.0
exc_count_above_threshold= list()
exc_pos_ratio_above_threshold =list()
exc_neg_ratio_above_threshold =list()

g4_str = "select distinct catch_exc  from "+ catch_training_table  
print " g4_str=",g4_str
select_cursor.execute(g4_str)
g4_db = select_cursor.fetchall()
unique_exc=list()
for d in g4_db:
    unique_exc.append(d[0])

print "len=", size(unique_exc)    
for temp_exc in unique_exc:
    #print temp_exc           
    exc_str = " select count(*)   from " + catch_training_table + " where catch_exc = '"+temp_exc+"'"
    select_cursor.execute(exc_str)
    data1 =  select_cursor.fetchall()
    
    total_count= 0
    for d in data1:
        total_count = d[0]
        
    if total_count >= total_count_threshold:
       
        pos_str = "select count(*)  from   " + catch_training_table +  "  where catch_exc = '"+ temp_exc+ "'  and is_catch_logged = 1"
        select_cursor.execute(pos_str)
        data2 = select_cursor.fetchall()
    
        pos_count = 0 
        for d in data2:  
            pos_count =d[0]     
        
        
        neg_str = "select count(*)  from   " + catch_training_table +  "  where catch_exc = '"+ temp_exc+ "'  and is_catch_logged = 0"
        select_cursor.execute(neg_str)
        data2 = select_cursor.fetchall()
    
        neg_count = 0 
        for d in data2:  
            neg_count =d[0]  
             
            
        pos_ratio = ((pos_count*100)/total_count)
        neg_ratio = ((neg_count*100)/total_count)
        
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
plt.savefig("F:\\Research\\Logging3\\result\\g-exc-ratio\\pos_ratio_tomcat.png",bbox_inches='tight')


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
plt.savefig("F:\\Research\\Logging3\\result\\g-exc-ratio\\neg_ratio_tomcat.png",bbox_inches='tight')






"""=====Not Used ===================#
g1_nl = "select AVG(try_loc) from "+ catch_training_table+ " where is_catch_logged=0"
select_cursor.execute(str1)
data1 = select_cursor.fetchall()
avg_try_loc_non_logged =  data1[0][0]

print "[STB]=", " Avg try Loc Logged=", avg_try_loc_logged, " Avg try Loc Non Logged=", avg_try_loc_non_logged



Graph 1
select_str = "select count(*) from " +table+ " where level=\"\""
print"select str=", select_str
select_cursor.execute(select_str)
function_without_log = select_cursor.fetchall()[0][0]
print "fucntion_with_0_log=", function_without_log

#Graph 1
#==================# 
log_1=0
log_2=0
log_3=0
log_4=0
log_more=0
log_count=list()
select_str = "select level from " +table+ " where level!=\"\""
select_cursor.execute(select_str)
data = select_cursor.fetchall()
for d in data:
    level= d[0].strip() 
    level=' '.join(level.split())
    length = len(level.split(" "))
    log_count.append(length)
    if length==1:
        log_1=log_1+1
    elif length==2:
        log_2=log_2+1 
    elif length==3:
        log_3=log_3+1
    elif length==4:
        log_4=log_4+1
    else:
        log_more=log_more+1  

print "log_1=", log_1
print "log_2=", log_2
print "log_3=", log_3
print "log_4=", log_4
print "log_more=", log_more

print "len=", length, level, log_count


#plt.title('Distribution of Log')
plt.ylabel('Function Count')
plt.xlabel('No. of Log Statements')
#plt.grid(True)
x=[1,2,3,4,5]
plt.xticks([1, 2, 3, 4,5], ['1', '2', '3', '4','>=5'])
log_count=[486,189,70,49,70]
plt.bar(x,log_count,width=0.3, align='center', color='green')
plt.plot(x, log_count, color='purple', lw=0.5, marker='s')
plt.savefig(file_path+"funcount-vs-log.eps")
plt.show()


#Graph 2
#================#
#Select all the tuple
select_str = "select method_content, level, method from " +table
select_cursor.execute(select_str)
data = select_cursor.fetchall()

method_body_loc=list()
method_body_noc=list()#Number of characters
log_count=list()
for d in data:
    method_content =d[0].strip()
    method_name = d[2].strip()
   # method_size = len(' '.join(method_content.split()))  #level=' '.join(level.split())
   # method_body_noc.append(method_size)
   
    method_loc = 0
    temp_method_content = method_content.split("\n")  #level=' '.join(level.split())
    #print "content", method_content
    for t in temp_method_content:
        if t:
            method_loc = method_loc+1
            
    method_body_loc.append(method_loc)
    
    level= d[1].strip() 
    print "level", level
    if not level:
        length=0
    else:    
        level=' '.join(level.split())
        length = len(level.split(" "))# No of log statements
    log_count.append(length)
    
    print "Method Name=", method_name,"LOC=", method_loc," log statement count=",length

#Plot Scatter Plot    
#========#      

plt.xlabel('Function Size(LOC)')
plt.ylabel('No. of Log Statements')
plt.scatter(method_body_loc, log_count,color='green')
plt.xlim([0,400])
plt.ylim([-1,25])
plt.savefig(file_path+"fun-scatter.eps")
plt.show()

#====================Graph 3===============#
#Removing outliers from the above figure
plt.xlabel('Function Size(LOC)')
plt.ylabel('No. of Log Statements')
plt.scatter(method_body_loc, log_count,color='red')
plt.xlim([0,250])
plt.ylim([-1,20])
plt.savefig(file_path+"fun-scatter-without-outliers.eps")

plt.show()


#=====================Graph 4================#
##To make box plot of log level and LOC
debug_method_loc=list()
error_method_loc=list()
info_method_loc=list()
warn_method_loc=list()
trace_method_loc=list()
fatal_method_loc=list()

select_str = "select method_content, level from " +table+" where level!=\"\""
select_cursor.execute(select_str)
data = select_cursor.fetchall()

for d in data:
    method_content = d[0].strip()
    method_loc = 0
    
    temp_method_content = method_content.split("\n")  #level=' '.join(level.split())
    #print "content", method_content
    for t in temp_method_content:
        if t:
            method_loc = method_loc+1
    
    info_flag=0
    error_flag=0
    trace_flag=0
    debug_flag=0
    warn_flag=0
    fatal_flag=0
    level= d[1].strip() 
    print "level", level
    level=' '.join(level.split())
    level_array=level.split(" ")
    for l in level_array:
        if l == "info":
            info_method_loc.append(method_loc)
        elif l=="error":
            error_method_loc.append(method_loc)
        elif l=="trace":
            trace_method_loc.append(method_loc)
        elif l=="debug":
            debug_method_loc.append(method_loc)
        elif l=="warn":
            warn_method_loc.append(method_loc)
        elif l=="fatal":
            fatal_method_loc.append(method_loc)

boxes=[]

boxes.append(debug_method_loc)
boxes.append(error_method_loc)
boxes.append(warn_method_loc)
boxes.append(info_method_loc)
boxes.append(trace_method_loc)
boxes.append(fatal_method_loc)
plt.figure()
plt.hold = True
plt.boxplot(boxes,vert=0)
labels=[" "," Debug"," Error"," Wran"," Info"," Trace"," Fatal"]
plt.yticks(range(len(labels)), labels, rotation=90, va="top", ha="center", fontsize=14)
plt.xlabel('Function Size(LOC)',fontsize=14)
plt.xlim([0,150])
plt.savefig(file_path+"level-vs-loc.eps")
plt.show()
#===========Graph 5=================#
select_str = "select method_content, level from " +table+" where level!=\"\""
select_cursor.execute(select_str)
data = select_cursor.fetchall()
method_body_sizes=list()
unique_log_count=list()

select_str = "select method_content, level from " +table+ " where level!=\"\""
select_cursor.execute(select_str)
data = select_cursor.fetchall()
for d in data:
    method_content =d[0].strip()
    method_size = len(' '.join(method_content.split()))  #level=' '.join(level.split())
    method_body_sizes.append(method_size)
    
    info_flag=0
    error_flag=0
    trace_flag=0
    debug_flag=0
    warn_flag=0
    fatal_flag=0
    level= d[1].strip() 
    print "level", level
    level=' '.join(level.split())
    level_array=level.split(" ")
    for l in level_array:
        if l == "info":
            info_flag=1
        elif l=="error":
            error_flag=1
        elif l=="trace":
            trace_flag=1
        elif l=="debug":
            debug_flag=1
        elif l=="warn":
            warn_flag=1
        elif l=="fatal":
            fatal_flag=1
    
    unique_level=info_flag+error_flag+trace_flag+debug_flag+warn_flag+fatal_flag
    
    print "unique level", unique_level
    unique_log_count.append(unique_level)

plt.xlabel('Function Size(NOC)')
plt.ylabel('No. of Different Log Levels Used')
plt.scatter(method_body_sizes, unique_log_count,color='red')
plt.show()

#====================Graph6==============================#
#==================heatMap================================#

info_count=0
trace_count=0
warn_count=0
fatal_count=0
debug_count=0
error_count=0
select_str = "select method, level from " +table+" where level!=\"\""
select_cursor.execute(select_str)
data = select_cursor.fetchall()
for d in data:
    method_name = d[0]
    
    info_count=0
    trace_count=0
    warn_count=0
    fatal_count=0
    debug_count=0
    error_count=0
    
    level= d[1].strip() 
    level=' '.join(level.split())
    level_array=level.split(" ")
    for l in level_array:
        total_log_lines = total_log_lines+1
        if l == "info":
            info_count=info_count+1
        elif l=="error":
            error_count=error_count+1
        elif l=="trace":
            trace_count=trace_count+1
        elif l=="debug":
            debug_count=debug_count+1
        elif l=="warn":
            warn_count=warn_count+1
        elif l=="fatal":
            fatal_count=fatal_count+1
    

#=================Table 1=================#
#This identifies how many log statment are their and what %percentage they are of total log statements
total_log_lines = 0
info_count=0
trace_count=0
warn_count=0
fatal_count=0
debug_count=0
error_count=0

select_str = "select level from " +table+" where level!=\"\""
select_cursor.execute(select_str)
data = select_cursor.fetchall()

for d in data:
    level= d[0].strip() 
    level=' '.join(level.split())
    level_array=level.split(" ")
    for l in level_array:
        total_log_lines = total_log_lines+1
        if l == "info":
            info_count=info_count+1
        elif l=="error":
            error_count=error_count+1
        elif l=="trace":
            trace_count=trace_count+1
        elif l=="debug":
            debug_count=debug_count+1
        elif l=="warn":
            warn_count=warn_count+1
        elif l=="fatal":
            fatal_count=fatal_count+1
    
print "Total_log_statements=",total_log_lines
print"info=",info_count
print"trace=",trace_count
print "warn=",warn_count
print "fatal=",fatal_count
print "debug=",debug_count
print "error=",error_count


#"""