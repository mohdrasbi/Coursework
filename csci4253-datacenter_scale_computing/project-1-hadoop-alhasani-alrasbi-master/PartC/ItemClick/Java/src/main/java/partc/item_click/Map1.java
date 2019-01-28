package partc.item_click;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map1 extends Mapper<LongWritable, Text, Text, IntWritable>
{
	private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();
    
	@Override
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException
	{
		String[] tokens = value.toString().split(",");
		String month = tokens[1].substring(0, 10).substring(5,7);
		String itemID = tokens[2];
		
		if(month.equals("04"))
		{
			word.set(itemID);
			context.write(word, one);
		}
	}
}