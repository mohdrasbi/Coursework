from pyspark.sql import SparkSession
from pyspark.context import SparkContext 
import re


def filter_words(line):
    '''
    Input: each line of file
    Output: list of words that are not stop words or empty strings
    '''

    stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
    regex = re.compile('[^a-zA-Z]')
    #get substring from line be removing unwanted characters for start and end of line
    words = line[16:len(line)-2].split()
    
    new_words = []
    for word in words:
        new_word = regex.sub('', word).lower()
        if((new_word not in stop_words) and (new_word != "")):
            new_words.append(new_word)
    
    return new_words

###########################

def get_output(rating, input_dir, output_dir):
    '''
    input: rating(1-5), input and output directories
    result: save words and their counts to output dir
    '''

    #get dataframe and save to input dir
    s = df.filter(df['overall'] == rating).select('reviewText')
    s.rdd.saveAsTextFile(input_dir)

    sc = SparkContext.getOrCreate()
    text_file = sc.textFile(input_dir)

    #map and reduce to get words counts
    counts = text_file.flatMap(filter_words).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortByKey(1)
    sorted_counts = counts.map(lambda x: (x[1], x[0])).sortByKey(0).map(lambda x: (x[1], x[0]))

    topDF = sorted_counts.toDF().limit(500)
    topRDD = topDF.rdd.map(tuple)
    topRDD.map(lambda x: "%s\t%s" %(x[0], x[1])).saveAsTextFile(output_dir)

###########################

my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb://student:student@ec2-54-210-44-189.compute-1.amazonaws.com/test.reviews") \
    .getOrCreate()

df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()


get_output(1.0, "bucket1/input", "bucket1/output")
get_output(2.0, "bucket2/input", "bucket2/output")
get_output(3.0, "bucket3/input", "bucket3/output")
get_output(4.0, "bucket4/input", "bucket4/output")
get_output(5.0, "bucket5/input", "bucket5/output")

