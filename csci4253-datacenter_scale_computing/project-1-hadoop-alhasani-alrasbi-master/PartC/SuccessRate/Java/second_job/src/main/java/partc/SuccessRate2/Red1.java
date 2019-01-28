package partc.SuccessRate2;

import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Red1 extends Reducer <LongWritable, Text, LongWritable, Text>
{
	public void reduce(LongWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException
	{
		float rate = 0;
		float bought = 0;
		float clicked = 0;
		
		int i = 0;
		
		Text t = new Text();
		String s;
		
		for(Text value: values)
		{
			if (i==0) {
				t = value;
				s = t.toString();
				clicked = Float.parseFloat(s);
			}
			else {
				t = value;
				s = t.toString();
				bought = Float.parseFloat(s);
			}
			i++;
		}
		
		if (bought > clicked)
			rate = clicked/bought;
		else
			rate = bought/clicked;

		context.write(key, new Text(""+rate));
	}
}
