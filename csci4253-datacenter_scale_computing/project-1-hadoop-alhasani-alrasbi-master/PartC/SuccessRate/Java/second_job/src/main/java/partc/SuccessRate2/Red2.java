package partc.SuccessRate2;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Red2 extends Reducer<FloatWritable, Text, Text, FloatWritable> {
	int counter = 0;
	public void reduce(FloatWritable key, Iterable<Text> list, Context context) throws java.io.IOException, InterruptedException {
		for (Text value : list) {
			if(counter == 10)
				return;
			context.write(value, key);
			counter ++;
		}
	}
}
