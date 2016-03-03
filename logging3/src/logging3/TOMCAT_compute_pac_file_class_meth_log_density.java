package logging3;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Iterator;
import java.util.List;

import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.Block;
import org.eclipse.jdt.core.dom.CatchClause;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.DoStatement;
import org.eclipse.jdt.core.dom.ForStatement;
import org.eclipse.jdt.core.dom.IfStatement;
import org.eclipse.jdt.core.dom.ImportDeclaration;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.Name;
import org.eclipse.jdt.core.dom.SimpleName;
import org.eclipse.jdt.core.dom.SwitchStatement;
import org.eclipse.jdt.core.dom.TryStatement;
import org.eclipse.jdt.core.dom.TypeDeclaration;
import org.eclipse.jdt.core.dom.VariableDeclarationFragment;
import org.eclipse.jdt.core.dom.WhileStatement;





/* @ Author: Sangeeta
 * @Uses:This file will be used to compute the logging density of file/packages/class/methods to make graphs
*/
public class TOMCAT_compute_pac_file_class_meth_log_density 

{
	String rawContent = "";
	String log_levels_combined = "";
	int file_LOC = 0;
	int file_SLOC  = 0 ;
	///*
	 String url = "jdbc:mysql://localhost:3306/";
	 String driver = "com.mysql.jdbc.Driver";
	 String db_name ="logging_level3";
	 String userName = "root"; 
	 String password = "1234";
	   
	//@Note: create this file using create_file_listing.py
	 String listing_file_path = "F:\\Research\\Logging3\\result\\tomcat-8.0.9_java_files.txt";
	 String logged_file_path = "F:\\Research\\Logging3\\result\\tomcat_log_all.txt";
	 String insert_table = "tomcat_file_logging_density";
	//*/
    
	/*
	 String url = "jdbc:mysql://localhost:3307/";
	 String driver = "com.mysql.jdbc.Driver";
	 String db_name ="logging_level3";
	 String userName = "sangeetal"; 
	 String password = "sangeetal";
	
	//@Note: create this file using create_file_listing.py
	 String listing_file_path = "E:\\Sangeeta\\Research\\Logging3\\result\\tomcat-8.0.9_java_files.txt";  
	 String logged_file_path = "E:\\Sangeeta\\Research\\Logging3\\result\\tomcat_log_all.txt";
	  String insert_table = "tomcat_file_logging_density";
   //*/
	 
	 Connection conn=null;	
     java.sql.Statement stmt = null;
     
     public static void main(String[] args) 
 	{
        TOMCAT_compute_pac_file_class_meth_log_density  demo = new TOMCAT_compute_pac_file_class_meth_log_density();
 		demo.conn = demo.initdb(demo.db_name);

 		if(demo.conn==null)
 		{
 			System.out.println(" Databasse connection is null");
 			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
 			try 
 			 {
 			  br.readLine();
 			 }catch(Exception e)
 			{}
 		}
 	    
 		//create new file for every run
 		try {
 		       BufferedWriter bw = new BufferedWriter(new FileWriter(demo.logged_file_path));
 		       bw.close();
 		      
 		       
 		} catch (IOException e1) 
 		  {
 		
 			e1.printStackTrace();
 		  }
               
 		
 		try {
 			BufferedReader br =  new BufferedReader(new FileReader(demo.listing_file_path));
 			String file_name =  br.readLine();
 			while(br!=null)
 			{
 				System.out.println("Parsing File="+file_name);
 				int len = (file_name.split("\\\\")).length;
 				//demo.complete_package_path = file_name.split("\\\\")[len-2];
 				//demo.temp_file_path= file_name.replace("\\", "\\\\");
 			  
 				demo.file_log_lines(file_name);
 				file_name =  br.readLine();
 				
 			}
 		} 
 		catch (FileNotFoundException e) 
 		{
 		   System.out.println("Error.. Can not open the listing file");
 			e.printStackTrace();
 		}
 		catch(IOException e)
 		{
 			e.printStackTrace();
 		}
 			
 	}
 	
 public void file_log_lines(String file_name)
 	{
	// System.out.println("  in func log lines");
	// file_name = "F:/Research/Logging3/dataset/tomcat-8.0.9/java/org/apache/juli/logging/Log.java" ;
	// file_name ="F:\\Research\\Logging3\\dataset\\tomcat-8.0.9\\java\\javax\\servlet\\jsp\\tagext\\BodyTag.java";
   //file_name = "F:\\Research\\Logging3\\dataset\\tomcat-8.0.9\\java\\org\\apache\\juli\\logging\\DirectJDKLog.java";
	 
	 util3_met u3m= new util3_met(); 
	 log_level_interface l = new log_level_interface();
	 Remove_Comments  rc =  new Remove_Comments();
	 
 		try
 		{
 			
 			file_LOC=0;
 			file_SLOC = 0;
 			int file_final_sloc = 0;
 			
 			file_LOC  = u3m.find_file_LOC(file_name); 	
 			String file_content_as_string = readFileToString(file_name);	
 			String file_content_without_comment =  rc.remove_comments(file_content_as_string);
 			 				 
 			l=  u3m.find_and_set_logging_level(file_content_without_comment, l);
			
 			
 			/*l.log_count = 2;
			l.log_levels_combined = "fd";
			l.logged=1;
 			file_SLOC=u3m.find_file_SLOC(file_content_as_string);*/
 			
 			
 			/***New code***/
 			
 			//	file_content_as_string  =  file_content_as_string.replaceAll("(/\\*([^*]|[\\r\\n]|(\\*+([^*/]|[\\r\\n])))*\\*+/)|(//.*)", "\n");
 			//  Link: Removing java comments: http://blog.ostermiller.org/find-comment
 			//	file_content_as_string  =  file_content_as_string.replaceAll("(/\\*([^*]|[\\r\\n]|(\\*+([^*/]|[\\r\\n])))*\\*+/)|(//.*)", "\n");
 			file_final_sloc= u3m.find_final_file_SLOC(file_content_without_comment);
 			/*************/
 			
 			
 			file_name=  file_name.replace("\\", "\\\\");
 	     	System.out.println(" file name="+ file_name+ " loc = "+ file_LOC+ " logged="+l.logged+  "new loc"+ file_final_sloc);
 			
 			insert_to_db(file_name, file_LOC, l.logged, l.log_count, l.log_levels_combined, file_SLOC, file_final_sloc);
 		}catch(Exception e){
 			
 			 e.printStackTrace();
 		}
 	
 	}
	 

private void insert_to_db(String file_name, int file_LOC2, int logged, int log_count,  String log_levels, int file_SLOC, int file_final_sloc)
{
	String insert_str = "insert into "+ insert_table + " values( '"+ file_name+"',"+ file_LOC2 +","+ logged+","+ log_count+",'"+log_levels+"',"+ file_SLOC+","+ file_final_sloc +")";
	
	Statement stmt =null;
	try 
	{
		stmt = conn.createStatement();
		stmt.executeUpdate(insert_str);
	} catch (SQLException e) 
	{
		e.printStackTrace();
	}

	
	
	
}

public Connection initdb(String db_name)
{
	 try {
		      Class.forName(driver).newInstance();
		      conn = DriverManager.getConnection(url+db_name,userName,password);
		      //System.out.println(" dbname="+ db_name+ "user name"+ userName+ " password="+ password);
		      if(conn==null)
		      {
		    	  System.out.println("Hi I am null :( :(");
		      }
		      
		 } catch (Exception e) 
		 {
		      e.printStackTrace();
		 }
		return conn;
}


public static String readFileToString(String filePath) throws IOException
	{
	    StringBuilder fileData = new StringBuilder(1000);
	    BufferedReader reader = new BufferedReader(new FileReader(filePath));

	    char[] buf = new char[10];
	    int numRead = 0;
	    while ((numRead = reader.read(buf)) != -1) {
	        //          System.out.println(numRead);
	        String readData = String.valueOf(buf, 0, numRead);
	        fileData.append(readData);
	        buf = new char[1024];
	    }
	    reader.close();
	    return  fileData.toString();    
 }
  

}
