package partc.item_click;

public class test {
	
	public static void main(String []args)
	{
		String value = "420374,2014-04-06T18:44:58.314Z,214537888,12462,1";
		String[] tokens = value.split(",");
		String month = tokens[1].substring(0, 10).substring(5,7);
		String itemID = tokens[2];
		
		if(month.equals("04"))
			System.out.println(itemID);
		else
			System.out.println(month);
	}
	
	
	
}
