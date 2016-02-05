

import lda

#==================================================================#
#  This file will be used to create LDA topics from the document
#==================================================================#


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

str1 = "select try_con from " +  catch_training_table  +  "    where is_catch_logged=1"
select_cursor.execute(str1)
data1= select_cursor.fetchall()