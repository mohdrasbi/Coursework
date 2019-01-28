package partc.SuccessRate2;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map2 extends Mapper<Text, Text, FloatWritable, Text> {
	public void map(Text key, Text value, Context context)
			throws java.io.IOException, InterruptedException {
		 // convert lines to string
        String line = value.toString();
         
        // split by tab
        String[] tokens = line.split("\t");
         
        // cast the numbers to integers
        Float new_value = Float.parseFloat(line);
         
        // output as integer key:text value
        context.write(new FloatWritable(new_value), key);
	}
}