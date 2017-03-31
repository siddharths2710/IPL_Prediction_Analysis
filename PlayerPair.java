import java.util.*;
import java.lang.*;
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;




public class PlayerPair{
	public static class Map extends Mapper<LongWritable, Text, Text, Text>{
	public void map(LongWritable key, Text value, Context con) throws IOException, InterruptedException
	{
			int run=0;
			String l = value.toString();
			String[] d=l.split(",");
			
		 	if(d.length > 8)
			{
				run = Integer.parseInt(d[7]);
				if(d[9].contains("caught") || d[9].contains("run out") || d[9].contains("bowled"))
				{
					con.write(new Text(d[4]), new(Text(d[6] + " " + -1)));
				} 
				else
				{
					con.write(new Text(d[4]), new(Text(d[6] + " " + run)));
				}
			}
			
		}	
  }
		public static class Reduce extends Reducer<Text, Text>
		{
			public void reduce(Text word, Iterable<Text> values, Context con) throws IOException, InterruptedException
			{
				int arr[] = {0,0,0,0,0,0,0,0};
				String res="";
				for(Text value : values)
   				{
   					int score =Integer.parseInt(value.toString().split(" ")[1]);	
					String bowler = value.toString().split(" ")[0];
					if(score == -1)
						arr[7]++;
					else
					{
						arr[score]++;
					}	
				}

		

				for (int i=0;i<arr.length - 1;i++) {
				 	res = res + arr[i] + ",";
					
				}
				res = res + arr[arr.length - 1];
				con.write(new Text(word.toString() + ","),new Text(res));
			}
		}

		public static void main(String [] args) throws Exception
		{

			Configuration c=new Configuration();
			//String[] files=new GenericOptionsParser(c,args).getRemainingArgs();
			Path input=new Path("/ipdata.csv"); //formatted data of ipl_match_formatted
			//Path input=new Path("/temp.csv");
			Path output=new Path("/singular_data_innings");

			Job j=Job.getInstance(c);
			j.setJobName("match");
			j.setJarByClass(PlayerPair.class);
			j.setMapperClass(Map.class);
		
			j.setMapOutputKeyClass(Text.class);
			j.setMapOutputValueClass(IntWritable.class);
			j.setCombinerClass(Reduce.class);																																																																					
			j.setReducerClass(Reduce.class);
			j.setOutputKeyClass(Text.class);
			j.setOutputValueClass(Text.class);
			FileInputFormat.addInputPath(j, input);
			FileOutputFormat.setOutputPath(j, output);
			System.exit(j.waitForCompletion(true)?0:1);

		}	
	
}
