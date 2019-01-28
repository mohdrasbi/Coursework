hadoop fs -mkdir imdb
hadoop fs -copyFromLocal input imdb/

spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.3.0 ../parta.py imdb/input imdb/output

hadoop fs -cat imdb/output/part-00000 | more
