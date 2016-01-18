package logging3;

public class test3
{


  public static void main(String args[])
  {
	  
	  String s  = "  s_logger.info(log(seq, Unable to send due to   + e.getMessage())); \n "+
			  	"	cancel(seq);    throw e; }";
	  String s2= "  log( IOException sending message ,e);";
	  String s3 = "  res.setStatus(400); " +
			  	"	res.setMessage( Invalid URI:   + ioe.getMessage()); " +
			   "		connector.logAccess(request,response,0,true);  " +
			   "	return false;  ";
	  
	  String s4="{ hbjbj  \n "+
 " log( Error closing redirector:   + ioe.getMessage(),Project.MSG_ERR);"+
"}";
  System.out.println("s4="+s4);

	  util3_met um = new util3_met();
	  log_level_interface l = new log_level_interface();
	  l =um.find_and_set_logging_level(s4, l);
	  
	  System.out.println(" l="+ l.log_count+  "  levels="+ l.log_levels_combined);
	  
  }
}
