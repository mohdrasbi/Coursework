package partc.SuccessRate2;

import org.apache.hadoop.fs.Path;

import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.mapreduce.lib.jobcontrol.ControlledJob;
import org.apache.hadoop.mapreduce.lib.jobcontrol.JobControl;

public class drive extends Configured implements Tool{
	@SuppressWarnings("deprecation")
	
	public int run(String[] args) throws Exception
	{
		JobControl jobControl = new JobControl("JobChain");
		Path inputPath = new Path(args[0]);
		Path inputPath2 = new Path(args[1]);
		Path outputPath = new Path(args[2]);
		
		//////////////
		
		Configuration conf1 = new Configuration();
		Job job1 = new Job(conf1);
		job1.setJarByClass(drive.class);
		
		job1.setOutputKeyClass(LongWritable.class);
		job1.setOutputValueClass(Text.class);
		job1.setMapperClass(Map1.class);
		job1.setReducerClass(Red1.class);
		job1.setOutputFormatClass(TextOutputFormat.class);
		
		MultipleInputs.addInputPath(job1, inputPath, TextInputFormat.class);
		MultipleInputs.addInputPath(job1, inputPath2, TextInputFormat.class);
		FileOutputFormat.setOutputPath(job1, new Path(outputPath, "temp"));
		
		ControlledJob controlledJob1 = new ControlledJob(conf1);
		controlledJob1.setJob(job1);
		jobControl.addJob(controlledJob1);
		
		//////////////
		
		Configuration conf2 = new Configuration();
		Job job2 = new Job(conf2);
        job2.setJarByClass(drive.class);
 
        job2.setMapperClass(Map2.class);
        job2.setReducerClass(Red2.class);
        job2.setNumReduceTasks(1);
 
        job2.setMapOutputKeyClass(FloatWritable.class);
        job2.setMapOutputValueClass(Text.class);
        job2.setOutputKeyClass(FloatWritable.class);
        job2.setOutputValueClass(Text.class);
        job2.setSortComparatorClass(FloatComparator.class);
         
        job2.setInputFormatClass(KeyValueTextInputFormat.class);
        FileInputFormat.addInputPath(job2, new Path(outputPath, "temp"));
 
        FileOutputFormat.setOutputPath(job2, new Path(outputPath, "final"));
//        job2.setOutputFormatClass(TextOutputFormat.class);
        
        ControlledJob controlledJob2 = new ControlledJob(conf2);
        controlledJob2.setJob(job2);
        
		//////////////
        
        // job2 dependent on job1
        controlledJob2.addDependingJob(controlledJob1);
        
        jobControl.addJob(controlledJob2);
        Thread jobControlThread = new Thread(jobControl);
        jobControlThread.start();
        
        while (!jobControl.allFinished()) 
        {
            System.out.println("Jobs in waiting state: " + jobControl.getWaitingJobList().size());  
            System.out.println("Jobs in ready state: " + jobControl.getReadyJobsList().size());
            System.out.println("Jobs in running state: " + jobControl.getRunningJobList().size());
            System.out.println("Jobs in success state: " + jobControl.getSuccessfulJobList().size());
            System.out.println("Jobs in failed state: " + jobControl.getFailedJobList().size());
	        try 
	        {
	            Thread.sleep(5000);
	        } 
	        catch (Exception e) 
	        {}

        } 
        
        System.exit(0);  
        return (job2.waitForCompletion(true) ? 0 : 1);	
	}
	
	public static void main(String[] args) throws Exception
	{
		int exitCode = ToolRunner.run(new drive(), args);
		System.exit(exitCode);
	}
}