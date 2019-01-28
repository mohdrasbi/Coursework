package partc.SuccessRate2;

import java.io.IOException;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

public class Map1 extends Mapper<LongWritable, Text, LongWritable, Text>
{
	@Override
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException
	{	
		String[] tokens = value.toString().split("\t");
		
		String itemID = tokens[0];
		String inforomation = tokens[1];
		
		LongWritable item = new LongWritable(Long.parseLong(itemID));
		
		Text info = new Text(inforomation);
		
		context.write(item, info);
	}
}