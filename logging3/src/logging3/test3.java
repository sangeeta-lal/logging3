package logging3;

public class test3
{


  public static void main(String args[])
  {
	  
	  String s  = "   s_logger.info(log(seq, Unable to send due to   + e.getMessage())); \n "+
			  	"	cancel(seq);    throw e; }";
	  String s2= "  log( IOException sending message ,e);";
	  String s3 = "  res.setStatus(400); " +
			  	"	res.setMessage( Invalid URI:   + ioe.getMessage()); " +
			   "		connector.logAccess(request,response,0,true);  " +
			   "	return false;  ";
	  
	  String s4="{ hbjbj  \n "+
 " log( Error closing redirector:   + ioe.getMessage(),Project.MSG_ERR);"+
"}";
	  
	  
	  String s5= "{  "+
  "String message= Cannot create JDBC driver of class    + (driverClassName != null ? driverClassName :   ) +    for connect URL   + url+  \n   ;  "+
  " logWriter.println(message); "+
  " t.printStackTrace(logWriter);  "+
 " throw new SQLException(message,t);  "+
"  }";

	  String s6= "{ "+
      " logDebug(e,key,1);  "+
     "  terminate(key);  "+
"   }";
  System.out.println("s5="+s5);

	  util3_met um = new util3_met();
	  log_level_interface l = new log_level_interface();
	  l =um.find_and_set_logging_level(s6, l);
	  
	  System.out.println(" l="+ l.log_count+  "  levels="+ l.log_levels_combined);
	  
  }
}
