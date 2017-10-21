package br.edu.positivo.wordTest;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Reducer.Context;

import br.edu.positivo.wordTest.WordCount.DescendingIntWritableComparable.DescendingKey;

/**
 * WordCount
 */
public class WordCount {

	// Define o processo de map
	public static class TokenizerMapper extends MapReduceBase
	// Recebe um objeto texto e retorna um texto em valor numerico
			implements Mapper<Object, Text, Text, IntWritable> {

		private final static IntWritable one = new IntWritable(1);
		private Text word = new Text();

		//
		public void map(Object key, Text value,
				OutputCollector<Text, IntWritable> collector, Reporter reporter)
				throws IOException {

			// Pega o texto, gera uma string e gera um array
			// "a a a a " => ["a", "a", "a", "a"]
			StringTokenizer itr = new StringTokenizer(value.toString());

			// Itera pelas palavras encontradas
			while (itr.hasMoreTokens()) {

				// Vai para o proximo item
				word.set(itr.nextToken());

				// Escreve no contexto a chave e o contador
				collector.collect(word, one);
			}
		}
	}

	// Representa o processo de reduce
	public static class IntSumReducer extends MapReduceBase implements
			Reducer<Text, IntWritable, Text, IntWritable> {

		// Recebe uma chave e um conjunto de valores
		// <p1, [1,1,1,1]>
		// e retorna um objeto chave => valor
		// <p1, 4>
		public void reduce(Text key, Iterator<IntWritable> values,
				OutputCollector<Text, IntWritable> collector, Reporter reporter)
				throws IOException {

			int sum = 0;

			// Soma os counts do array
			while (values.hasNext()) {
				sum += values.next().get();
			}

			collector.collect(key, new IntWritable(sum));
		}
	}

	public static class SortMapper extends MapReduceBase implements
			Mapper<Object, Text, IntWritable, Text> {

		public void map(Object key, Text value,
				OutputCollector<IntWritable, Text> collector, Reporter args)
				throws IOException {

			StringTokenizer stringTokenizer = new StringTokenizer(
					value.toString());
			{
				int number = 999;
				String word = "empty";

				// A primeira posicao e o texto
				if (stringTokenizer.hasMoreElements()) {
					String str0 = stringTokenizer.nextToken();
					word = str0.trim();
				}

				// A segunda posicao e o count
				if (stringTokenizer.hasMoreElements()) {
					String str1 = stringTokenizer.nextToken();
					number = Integer.parseInt(str1.trim());
				}

				collector.collect(new IntWritable(number), new Text(word));
			}
		}
	}

	public static class SortReducer extends MapReduceBase implements
			Reducer<IntWritable, Text, IntWritable, Text> {
		
		ArrayList<String> list = new ArrayList<String>();

		public void reduce(IntWritable key, Iterator<Text> words,
				OutputCollector<IntWritable, Text> collector, Reporter reporter)
				throws IOException {

	        while (words.hasNext()) {
				list.add(words.next().toString());
	        }

			Collections.sort(list);

			for (String val : list) {
				collector.collect(key, new Text(val));
			}

			list.clear();
		}
	}

	public static class DescendingIntWritableComparable extends IntWritable {
		public static class DescendingKey extends Comparator {

			@SuppressWarnings("rawtypes")
			public int compare(WritableComparable a, WritableComparable b) {
				return -super.compare(a, b);
			}

			public int compare(byte[] b1, int s1, int l1, byte[] b2, int s2,
					int l2) {
				return -super.compare(b1, s1, l1, b2, s2, l1);
			}
		}
	}

	public static class TextPartitioner extends Partitioner<Text, NullWritable> {
		public int getPartition(Text word, NullWritable nullWritable,
				int numPartitions) {
			return word.hashCode() % numPartitions;
		}
	}

	public class TextGroupingComparator extends WritableComparator {
		public TextGroupingComparator() {
			super(Text.class, true);
		}

		@SuppressWarnings("rawtypes")
		@Override
		public int compare(WritableComparable k1, WritableComparable k2) {
			Text w1 = (Text) k1;
			Text w2 = (Text) k2;
			return w1.compareTo(w2);
		}
	}

	// Gera o job no hadoop (BOILERPLATE)
	// Todo job tem um map
	@SuppressWarnings("deprecation")
	public static void main(String[] args) throws Exception {
		// Primeiro job (conta palavras)
		JobConf conf = new JobConf(WordCount.class);

		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(IntWritable.class);

		conf.setMapperClass(TokenizerMapper.class);
		conf.setCombinerClass(IntSumReducer.class);
		conf.setReducerClass(IntSumReducer.class);

		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path("/tmp/temp"));

		Job wordCountJob = new Job(conf, "Word Count");

		// Segundo job (ordena por count)
		JobConf sortJobConf = new JobConf(WordCount.class);
		sortJobConf.setJobName("Word Count (Sort)");

		sortJobConf.setOutputKeyClass(Text.class);
		sortJobConf.setOutputValueClass(IntWritable.class);

		sortJobConf.setMapperClass(SortMapper.class);
		sortJobConf.setCombinerClass(SortReducer.class);
		sortJobConf.setReducerClass(SortReducer.class);

		// Set the key-value pair output format
		sortJobConf.setMapOutputKeyClass(IntWritable.class);
		sortJobConf.setMapOutputValueClass(Text.class);

		// Sort desceding
		sortJobConf.setOutputKeyComparatorClass(DescendingKey.class);

		sortJobConf.setInputFormat(TextInputFormat.class);
		sortJobConf.setOutputFormat(TextOutputFormat.class);

		FileInputFormat.setInputPaths(sortJobConf, new Path(
				"/tmp/temp/part-00000"));
		FileOutputFormat.setOutputPath(sortJobConf, new Path(args[1]));

		Job wordCountSortJob = new Job(sortJobConf);

		// Executa job
		wordCountJob.submit();

		if (wordCountJob.waitForCompletion(true)) {
			wordCountSortJob.submit();
			wordCountSortJob.waitForCompletion(true);
		}
	}
}
