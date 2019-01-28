from pyspark.sql import SparkSession
import pyspark.sql.functions as func


def outputTopRated(metadata, reviews, category):
	'''
	Input: metadata and reviews collections, and category name
	Output: Top 1 product in a certain category
	'''

	cate_filtered = metadata.filter(func.array_contains(metadata["categories"], category))

	#join cate_filtered dataframe with reviews collection
	#and select id, title and overall columns
	inner_join = cate_filtered.join(reviews, cate_filtered.asin == reviews.asin).select(cate_filtered['asin'], 'title', 'overall')

	#map each row to a list
	map_join = inner_join.rdd.map(list)

	#map: (id, title) is key, (rating, 1) is value
	#reduce: sum all ratings and all 1s (which is gonna be num of reviews)
	counts = map_join.map(lambda x: ((x[0], x[1]), (x[2], 1))).reduceByKey(lambda a, b: (a[0]+b[0], a[1]+b[1])).sortBy(lambda x: x[1])
	counts = counts.map(lambda x: [category, x[0][1], x[1][0], x[1][1]]).sortBy(lambda x: float(x[2])/float(x[3]), ascending=False)
	countsDF = counts.toDF()

	#get the products with num of reviews > 100
	countsDF_filtered = countsDF.filter(countsDF[3] > 100)

	return countsDF_filtered.limit(1)

###########################

reviews_session = SparkSession \
    .builder \
    .config("spark.mongodb.input.uri", "mongodb://student:student@ec2-54-210-44-189.compute-1.amazonaws.com/test.reviews") \
    .getOrCreate()

reviews = reviews_session.read.format("com.mongodb.spark.sql.DefaultSource").load()

metadata_session = SparkSession \
    .builder \
    .config("spark.mongodb.input.uri", "mongodb://student:student@ec2-54-210-44-189.compute-1.amazonaws.com/test.metadata") \
    .getOrCreate()

metadata = metadata_session.read.format("com.mongodb.spark.sql.DefaultSource").load()

###########################

movies_tv = outputTopRated(metadata, reviews, "Movies & TV")
cds_vinyl= outputTopRated(metadata, reviews, "CDs & Vinyl")
video_games = outputTopRated(metadata, reviews, "Video Games")
toys_games = outputTopRated(metadata, reviews, "Toys & Games")

top = movies_tv.union(cds_vinyl).union(video_games).union(toys_games)
top.rdd.sortBy(lambda x: x[0]).map(lambda x: "%s\t%s\t%s\t%f" %(x[0], x[1], x[3], float(x[2])/float(x[3]))) \
	        .saveAsTextFile("part1")


