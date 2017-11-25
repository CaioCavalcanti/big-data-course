# MapReduce - Final Project
This project has a MapReduce process that list all words from all files in a given directory in HDFS, in reverse alphabetical order.

## Requirements
You should basically use [Cloudera Quickstart VM 5.12](https://www.cloudera.com/downloads/quickstart_vms/5-12.html), as it has all you need to run this project.

## How to execute it
1. Clone this repository
```
$ git clone https://github.com/CaioCavalcanti/big-data-course.git
```
2. Open this project on eclipse, wait maven restore the dependencies and create a new maven build (~~there might be a better way to do this~~)
3. Run the build and check the result on the target folder
```
$ ls ~/project/path/target
classes  ListWords-0.0.1-SNAPSHOT.jar  maven-archiver  test-classes
```
4. Create an input directory on HDFS and send your files to it
```
$ hdfs dfs -mkdir input
$ hdfs dfs -put ~/files/path input
```
5. Run the application from the JAR file, passing the paths to the input and output directories in HDFS
```
$ hadoop jar ListWords-0.0.1-SNAPSHOT.jar com.caio.hadoop.mapreduce.finalProject.ListWords input output
```
6. Checkout the output
```
$ hdfs dfs -cat output/*
yellow    2
what      1
Oh        1
is        3
Hadoop    3
fellow    1
elephant  1
can       1
be        1
as        2
an        1
a         1
```

## What does it do?
```
TODO: Explain the code line-by-line
```