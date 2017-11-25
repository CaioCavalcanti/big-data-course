**If you don't want to spend some time configuring the environment, you can just use  [Cloudera Quickstart VM for CDH 5.12](https://www.cloudera.com/downloads/quickstart_vms/5-12.html)**

First we need to send the files to HDFS. For this exercise I've used some articles I found about Spark, you can find it on [articles](Articles).
```
$ hdfs dfs -mkdir /user/cloudera/input
$ hdfs dfs -put articles /user/cloudera/input
$ hdfs dfs -ls /user/cloudera/input/articles
Found 4 items
-rw-r--r--   1 cloudera cloudera      42284 YYYY-MM-DD HH:mm /user/cloudera/input/articles/Apache Spark Tutorial ML with PySpark
-rw-r--r--   1 cloudera cloudera      31830 YYYY-MM-DD HH:mm /user/cloudera/input/articles/Apache Spark in Python Beginners Guide
-rw-r--r--   1 cloudera cloudera      30858 YYYY-MM-DD HH:mm /user/cloudera/input/articles/Spark Cluster Computing with Working Sets
-rw-r--r--   1 cloudera cloudera       8678 YYYY-MM-DD HH:mm /user/cloudera/input/articles/Why you should use Spark for machine learning
```

For convenience I've used Spark from command line, you can open it executing the following command

```
$ spark-shell --master yarn
```

Let's wait until it loads evertything and shows the welcome message, it can take some time, depending on you machine/VM specs. You'll know it's ready when you see this:

```
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel).
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/usr/lib/zookeeper/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/lib/flume-ng/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/lib/parquet/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/lib/avro/avro-tools-1.7.6-cdh5.12.0.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 1.6.0
      /_/

Using Scala version 2.10.5 (Java HotSpot(TM) 64-Bit Server VM, Java 1.7.0_67)
Type in expressions to have them evaluated.
Type :help for more information.
Spark context available as sc (master = yarn-client, app id = application_1510507948748_0001).
SQL context available as sqlContext.

scala> 
```

For now we'll use [Scala](https://www.scala-lang.org/) to make the magic happens on Spark.

Now that all files are inside HDFS and we're are on Spark, we need to get the files using the command ```wholeTextFiles(path)```. This command will read all documents available on the path you inform

```
scala> val files = sc.wholeTextFiles("/user/cloudera/input/articles")
files: org.apache.spark.rdd.RDD[(String, String)] = input/articles MapPartitionsRDD[1] at wholeTextFiles at <console>:27
```

As you can see on the result it will result in a [RDD](https://www.tutorialspoint.com/apache_spark/apache_spark_rdd.htm) containing an ```Array[(String, String)]``` with some key-value pairs, known as [tuples](https://alvinalexander.com/scala/scala-tuple-examples-syntax). The key will be the name of the file, and the value will be the whole content of the file as string.

But for this exercise, we need to analyze only the content of all files, so we need to transform the key-value pair array (```Array[(String, String)]```) into a array of strings (```Array[String]```). To do this we need to use the ```map{ case (key, value) => ... }``` function, as we are working with a tuple.

```
scala> val contents = files.map{ case (fileName, content) => content }
content: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[2] at map at <console>:29
```

Basically this command is reading each file of the ```files``` array and mapping the content of it to the  ```contents``` RDD, which is an ```Array[String]```.

Now we have a array of files, but we still need to do some work to get there. The next step is to break each file into lines. We can do this executing the command below:.


```
scala> val allLines = contents.flatMap(file => file.split("\n"))
allLines: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[3] at flatMap at <console>:31
```

With this function we got the content of each file, split it using the line breaker ("\n") and combined the result into an RDD of  ```Array[String]```, called ```allLines```.

We need to use ```flatMap()``` because the the ```split()``` function returns an array of strings for each file and the ```flatMap()``` help us combining those arrays into a single one, resulting in a ```Array[String]``` instead of ```Array[Array[String]]```. You can find a better explanation [here](https://data-flair.training/blogs/apache-spark-map-vs-flatmap/).

Now that we have all lines, let's break it into words, using the same command above, but spliting it on blank spaces (" ") instead of line-breakers ("\n")

```
scala>val allWords = allLines.flatMap(line => line.split(" "))
allWords: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[4] at flatMap at <console>:33
```

Now we have an RDD of ```Array[String]`` with all words of all files, so far, so good!

We can check how many words we have and how many are unique using ```count``` and ```distinct```, as below

```
scala> allWords.count
res0: Long = 18832

scala> allWords.distinct.count
res1: Long = 4132 
```

Before we count each word, let's clean it, as it may have some noisy characters, such as "word," and "word.", and it's case sensitive, so we need to normalize everything and remove possible empty string. Let's do this!

```
scala> val allClean = allWords.map(word => word.replaceAll("[$,?+.;:\'s\\W\\d]", "").toLowerCase).filter(_.nonEmpty)
allClean: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[5] at map at <console>:35
```

If we check the word and distinct count again, we'll see that we've reduced the number of words.

```
scala> allClean.count
res3: Long = 17263

scala> allClean.distinct.count
res4: Long = 2312 
```

Now that we have a list of all words we can easily check how many times each one appears, using the ```countByValue()``` function. You can check it calling ```allClean.countByValue```.

If we wanted only the list of all words, that would be enough, we could just save it and check the results. But we can go a little further, let's get the words count.

```
scala> val wordCount = allClean.map(word => (word, 1)).reduceByKey(_ + _)
wordCount: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[6] at reduceByKey at <console>:39
```

And sort it to check see the most commons first

```
scala> val sorted = wordCount.sortBy(_._2, false)
sorted: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[7] at sortBy at <console>:37
```

All good, let's save the results!

```
scala> sorted.saveAsTextFile("/user/cloudera/output/Articles")
```

Let's see what we've got on HDFS, in a new terminal server (or we can leave Spark using ```exit``` command) execute the following command list the files

```
$ hdfs dfs -ls /user/cloudera/output/articles
Found 3 items
-rw-r--r--   1 cloudera cloudera          0 YYYY-MM-DD HH:mm /user/cloudera/output/articles/_SUCCESS
-rw-r--r--   1 cloudera cloudera       9745 YYYY-MM-DD HH:mm /user/cloudera/output/articles/part-00000
-rw-r--r--   1 cloudera cloudera      19997 YYYY-MM-DD HH:mm /user/cloudera/output/articles/part-00001
```

Now we just need to work with the ```part-*``` files to see the results!

```
$ hdfs dfs -cat /user/cloudera/output/articles/part-00000

(the,931)
(to,616)
(a,548)
(you,398)
(and,388)
(of,361)
(that,334)
(in,305)
(spark,253)
(i,229)
(data,211)
(with,188)
(thi,177)
(can,170)
(for,165)
(it,164)
(rdd,142)
(on,140)
(are,119)
(your,113)
(ue,106)
(be,94)
(or,91)
(have,83)
(by,83)
(which,80)
(when,76)
(an,74)
(dataframe,72)
(from,71)
[...]
```

[Contact me](mailto:caiofabiomc@gmail.com) if you need any help :)