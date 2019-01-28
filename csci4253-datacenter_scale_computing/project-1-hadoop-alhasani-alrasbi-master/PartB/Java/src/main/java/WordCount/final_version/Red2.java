package WordCount.final_version;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Red2 extends Reducer<IntWritable, Text, Text, IntWritable> {
	
	public void reduce(IntWritable key, Iterable<Text> list, Context context) throws java.io.IOException, InterruptedException {
		for (Text value : list) {
			context.write(value, key);
		}
	}
}