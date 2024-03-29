package partc.SuccessRate;
import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Red1 extends Reducer <Text, IntWritable, Text, IntWritable>
{
	public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException
	{
		int sum = 0;
		while(values.iterator().hasNext())
		{
			sum += values.iterator().next().get();
		}
		context.write(key, new IntWritable(sum));
	}
}
