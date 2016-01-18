package logging3;

public class test3
{


  public static void main(String args[])
  {
	  
	  String s  = "  s_logger.info(log(seq, Unable to send due to   + e.getMessage())); \n "+
			  	"	cancel(seq);    throw e; }";
	  String s2= "  log( IOException sending message ,e);";
	  util3_met um = new util3_met();
	  log_level_interface l = new log_level_interface();
	  l =um.find_and_set_logging_level(s2, l);
	  
	  System.out.println(" l="+ l.log_count+  "  levels="+ l.log_levels_combined);
	  
  }
}
