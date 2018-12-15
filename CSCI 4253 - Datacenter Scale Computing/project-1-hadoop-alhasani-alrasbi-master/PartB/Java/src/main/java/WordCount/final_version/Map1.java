package WordCount.final_version;
import java.io.IOException;
import java.util.Arrays;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map1 extends Mapper<LongWritable, Text, Text, IntWritable>
{
  private final static IntWritable one = new IntWritable(1);
  private Text word = new Text();
   
  public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException
  {
      //Stop Words
      String stopWord = "a about above after again against all am an and any are aren't as at be because been before being below "
              + "between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further "
              + "had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if "
              + "in into is isn't it it's its itself let's me more most mustn't my myself no nor  not of off on once only or other ought our ours ourselves out over own same "
              + "shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're "
              + "they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom "
              + "why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves";
      String[] stopWords = stopWord.split(" ");
      for (int i = 0; i<stopWords.length; i++)
      {
          stopWords[i] = stopWords[i].replaceAll("[^a-zA-Z]","").toLowerCase();
      }
       
      //1) Take in text from a file. Lowercase everything, split by space. 
      String words[] = value.toString().toLowerCase().split(" ");
       
      //2) Remove punctuation
      for (int i = 0; i<words.length; i++)
      {   
          if(words[i] != null) 
              words[i] = words[i].replaceAll("[^a-zA-Z]","");
      }
      //3) check if stopWord, if so, make it null
      for (int i = 0; i<words.length; i++)
      {   
          if(words[i] != null && Arrays.asList(stopWords).contains(words[i]) == true) 
              words[i] = null;
      }
       
      for (int i = 0; i<words.length; i++)
      {
          if (words[i] != null)
          {
              // create a set (unique elements) from the array
              word.set(words[i]);
              context.write(word, one);
          }
      }
  }
}