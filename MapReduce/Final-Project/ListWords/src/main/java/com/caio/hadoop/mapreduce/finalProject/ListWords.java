package com.caio.hadoop.mapreduce.finalProject;

import java.io.IOException;
import java.util.Iterator;
import java.util.StringTokenizer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.io.WritableComparator;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.mapreduce.Job;

/**
 * List Words UP - Big Data - Final project Author Caio Cavalcanti
 *
 */
public class ListWords {

	public static class Map extends MapReduceBase implements
			Mapper<Object, Text, Text, NullWritable> {
		NullWritable out = NullWritable.get();
		private Text word = new Text();

		public void map(Object key, Text value,
				OutputCollector<Text, NullWritable> collector, Reporter reporter)
				throws IOException {

			StringTokenizer itr = new StringTokenizer(value.toString());

			while (itr.hasMoreTokens()) {
				word.set(itr.nextToken());
				String lower = word.toString().toLowerCase();

				collector.collect(new Text(lower), out);
			}
		}
	}

	public static class Reduce extends MapReduceBase implements
			Reducer<Text, IntWritable, Text, NullWritable> {
		NullWritable out = NullWritable.get();

		public void reduce(Text key, Iterator<IntWritable> values,
				OutputCollector<Text, NullWritable> collector, Reporter reporter)
				throws IOException {
			collector.collect(key, out);
		}
	}

	public static class DescendingKey extends WritableComparator {
		protected DescendingKey() {
			super(Text.class, true);
		}

		@SuppressWarnings("rawtypes")
		@Override
		public int compare(WritableComparable w1, WritableComparable w2) {
			Text key1 = (Text) w1;
			Text key2 = (Text) w2;
			return -1 * key1.compareTo(key2);
		}
	}

	@SuppressWarnings("deprecation")
	public static void main(String[] args) throws Exception {
		JobConf conf = new JobConf(ListWords.class);

		conf.setMapOutputKeyClass(Text.class);
		conf.setMapOutputValueClass(NullWritable.class);

		conf.setMapperClass(Map.class);
		conf.setCombinerClass(Reduce.class);
		conf.setReducerClass(Reduce.class);

		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);

		conf.setOutputKeyComparatorClass(DescendingKey.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));

		Job listWordSortJob = new Job(conf, "List words descending");

		System.exit(listWordSortJob.waitForCompletion(true) ? 0 : 1);
	}
}
