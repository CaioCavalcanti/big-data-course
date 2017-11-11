## Important
For those exercises I'm assuming that:
- Spark is being used inside [Cloudera Quickstart VM for CDH 5.12](https://www.cloudera.com/downloads/quickstart_vms/5-12.html)
- All input files have been already sent to ```input``` directory on HDFS

## 1. Reading all files in a directory and getting all words
```
# Read all files on HDFS input directory
val allFiles = sc.wholeFileText('input').map{ case(fileName, content) => content }
# Split the files by line-break into array
val allLines = allFiles.flatMap(file => file.split('\n'))
# Split the lines by white space into array
val allWords = allLines.flatMap(line => line.split(' '))
```

## 2. Counting words in a file
After executing #1
```
```

## 3. Filtering words
After executing #1
```
```

## 4. Sorting words by length
After executing #1
```
```

## 5. Getting average from array of numbers
```
```
