from pyspark.sql import SparkSession
from pyspark.context import SparkContext 
import sys


inDir = sys.argv[1]
outDir = sys.argv[2]
key1 = sys.argv[3]
key2 = sys.argv[4]

sc = SparkContext()
spark = SparkSession(sc)

sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", key1)
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", key2)
text_file = sc.textFile(inDir)

counts = text_file.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortByKey(1)
sorted_counts = counts.map(lambda x: (x[1], x[0])).sortByKey(0).map(lambda x: (x[1], x[0]))

sorted_counts.map(lambda x: "%s\t%s" %(x[0], x[1])).saveAsTextFile(outDir)
