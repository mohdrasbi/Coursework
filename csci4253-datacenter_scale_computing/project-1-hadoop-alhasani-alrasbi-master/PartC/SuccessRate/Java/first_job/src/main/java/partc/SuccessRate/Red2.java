package partc.SuccessRate;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Red2 extends Reducer<IntWritable, Text, LongWritable, Text> {

	public void reduce(IntWritable key, Iterable<Text> list, Context context) throws java.io.IOException, InterruptedException {
		
		String s = key.toString();
		LongWritable final_key = new LongWritable(Long.parseLong(s));
		
		for (Text value : list) {
			context.write(final_key, value);
		}
	}
}
