```
hdfs dfs -mkdir input
hdfs dfs -put ~/articles input
spark-shell --master yarn

val files = sc.wholeTextFiles("input/articles")
val contents = files.map{ case (fileName, content) => content }
val allLines = contents.flatMap(file => file.split("\n"))
val allWords = allLines.flatMap(line => line.split(" "))
val result = allWords.map(word => word.toLowerCase).distinct().sortBy(_.toString, false)
result.saveAsTextFile("output/listWordsSpark")

hdfs dfs -cat output/listWordsSpark/part-*
```