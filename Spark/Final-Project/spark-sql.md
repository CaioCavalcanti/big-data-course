```
hdfs dfs -mkdir input
hdfs dfs -put ~/articles input
spark-shell --master yarn

val files = sc.wholeTextFiles("input/articles")
val contents = files.map{ case (fileName, content) => content }
val allLines = contents.flatMap(file => file.split("\n"))
val allWords = allLines.flatMap(line => line.split(" "))

val df = allWords.toDF()
val sorted = df.distinct().sort($"_1".desc)
val rdd = sorted.rdd
val result = rdd.map(row => row(0).toString)

result.saveAsTextFile("output/listWordsSparkSql")

hdfs dfs -cat output/listWordsSparkSql/part-*
```