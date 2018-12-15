package WordCount.final_version;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map2 extends Mapper<LongWritable, Text, IntWritable, Text> {
	public void map(LongWritable key, Text value, Context context)
			throws java.io.IOException, InterruptedException {
		 // convert lines to string
        String line = value.toString();
         
        // split by tab
        String[] tokens = line.split("\t");
         
        // cast the numbers to integers
        int new_value = Integer.parseInt(tokens[1]);
         
        // output as integer key:text value
        context.write(new IntWritable(new_value), new Text(tokens[0]));
	}
}