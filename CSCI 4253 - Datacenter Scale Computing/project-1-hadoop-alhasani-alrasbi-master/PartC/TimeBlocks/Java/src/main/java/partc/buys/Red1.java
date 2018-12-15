package partc.buys;

import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Red1 extends Reducer <Text, IntWritable, Text, IntWritable>
{
	public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException
	{
		int sum = 0;
		/* 
		 * iterate through the values of a key 
		 * hasNext(): boolean method that checks if there is
		 * another value to iterate over
		 */
		while(values.iterator().hasNext())
		{
			// sum over all the values
			// next(): finds and returns the next complete token
			// get(): fetches an element from the list
			sum += values.iterator().next().get();
		}
		context.write(key, new IntWritable(sum));
	}
}
