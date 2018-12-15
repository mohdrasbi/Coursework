package partc.buys;

import java.io.IOException;
//import java.util.Arrays;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map1 extends Mapper<LongWritable, Text, Text, IntWritable>
{
	@Override
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException
	{
		// split each line by commas
		String[] tokens = value.toString().split(",");
		
		// store time 
		String buyTime = tokens[1].substring(11,13);
		
		// store price
		String price = tokens[3];
		
		String quantity = tokens[4];
		
		// convert String(s) to Int(s)
		IntWritable revenue = new IntWritable(Integer.parseInt(quantity)*Integer.parseInt(price));
		
		// convert string to Text
		Text buying = new Text(buyTime);
		
		buying.set(buying);
		
		context.write(buying, revenue);
	}
}