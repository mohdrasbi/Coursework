import pandas as pd
import glob
from difflib import SequenceMatcher
import time
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from sklearn import feature_extraction
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import nltk
import matplotlib.pyplot as plt


def addToPrev(prev, index, text):
    prev[index] = text
    return prev

def inPrev(prev, text, tot_sims):
    for message in prev:
        if SequenceMatcher(None, text, message).ratio() >= 0.7:
            tot_sims.setdefault(message, []).append(text)
            return True, tot_sims
    return False, tot_sims

def reduce_tweets(tweets, times, reduceBy): 
    prev = [""]*reduceBy
    index = 0
    tot_sims = {}
    filtered_tweets = []
    filtered_times = []
    
    for _tweet, _time in zip(tweets, times):
        in_prev, tot_sims = inPrev(prev, _tweet, tot_sims)
        if not in_prev:
            prev = addToPrev(prev, index, _tweet)
            index = (index + 1) % reduceBy
            filtered_tweets.append(_tweet)
            filtered_times.append(_time)
    
    return filtered_tweets, filtered_times

def check_sim(check_word):
    words = ["mosquito", "protect", "repel", "spray"]
    for word in words:
        if SequenceMatcher(None, check_word, word).ratio() >= 0.7:
            return True
    return False

def times_hist(times):
    hour_blocks = []
    for i in times:
        #times element example: 2016-09-28T00:00:10.000Z
        temp = i.split("T")[1].split(":") 
        hour = int(temp[0])
        hour_blocks.append(hour)

    bins = [i for i in range(0, 25)]
    plt.hist(hour_blocks, edgecolor='white', bins=bins, align='left')
    plt.xticks(bins[:-1])
    plt.xlabel("Hour block")
    plt.ylabel("Number of tweets")
    plt.title("Tweets over time")
    plt.show()

def create_bucket(tweets, times, spec_time):
    new_tweets = []
    new_times = []
    for i in range(len(times)):
        hour = int(times[i].split("T")[1].split(":")[0])
        if hour == spec_time:
            new_tweets.append(tweets[i])
            new_times.append(times[i])

    return new_tweets, new_times
            

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

stemmer = SnowballStemmer("english")

def centers_for_clusters(finalSample):
    tfidf_vector = TfidfVectorizer(max_df=0.7, #max_features=200000,
                                     min_df=9, stop_words='english',
                                     use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

    matrix = tfidf_vector.fit_transform(finalSample) #fit the matrixizer to personal tweets

    print("----------- Matrix Shape -----------")
    print(matrix.shape)
    feature_names = tfidf_vector.get_feature_names()
    print("")
    print("----------- Features -----------")
    print("Feature Length: ", len(feature_names))
    print()
    return feature_names

def best_center(center):
    max = 0
    final_center = ''
    for element in center:
        if len(element) > max:
            max = len(element)
            final_center = element
    return final_center

def first_reduction(feature_names):
    possibleCenters = []
    print("Original Length: ", len(feature_names))
    for i, feature in enumerate(feature_names):
        # some features are only a single letter, not helpful
        if len(feature) > 2: 
            similarCenters = [feature]
            # 100, 200 , 500, and 'n' all give the same result
            # hence, 100 will do 
            for feature2 in feature_names[i:i+100]:
                if feature != feature2:
                    if SequenceMatcher(None, feature, feature2).ratio() > 0.6:
                        similarCenters.append(feature2)
            possibleCenters.append(similarCenters)


    final_list = []
    for element in possibleCenters:
        element = sorted(element)
        final_list.append(element)

    final_list = sorted(final_list)
    print("First Reduction: ", len(final_list))
    return final_list
    
def combine_centers(final_list):
    centers = [final_list[0]]
    print("Original Length: ", len(final_list))
    for i in range(len(final_list)-1):
        a = final_list[i]
        b = final_list[i+1]
        similarity = SequenceMatcher(None, a, b).ratio()
        if i > 0 and similarity < 0.2:
            centers.append(final_list[i])
            
    previous_center = centers[0]

    centers2 = [best_center(previous_center)]

    # iterate through centers starting at the second element 
    for i in range(len(centers)):
        similarity = SequenceMatcher(None, ''.join(previous_center), ''.join(centers[i])).ratio()
        if i > 0 and similarity < 0.25:
            word_to_add = best_center(centers[i])
            if word_to_add not in centers2 and word_to_add != 'rt':
                centers2.append(word_to_add)
                previous_center = centers[i]

    centers2 = sorted(centers2)
    print()
    print("Reduced Length: ", len(centers2))
    return centers2

def create_clusters(centers, input_tweets):
    dictionary = dict.fromkeys(centers)
    finalSample2 = sorted(input_tweets)
    finalSample3 = []
    leftOvers = []

    for tweet in finalSample2:
        stemmed = tokenize_and_stem(tweet)
        stemmed = ' '.join(stemmed)
        check = 1
        for center in centers:
            if center in tweet.lower():
                check = 0
                if dictionary[center] != None:
                    dictionary[center].append(tweet)
                else:
                    dictionary[center] = [tweet]
                break

        if check == 1:
            finalSample3.append(tweet)

    for tweet in finalSample3:
        stemmed = tokenize_and_stem(tweet)
        stemmed = ' '.join(stemmed)
        check = 1

        for center in centers:
            similarity = SequenceMatcher(None, center, stemmed).ratio()

            if similarity > 0.25 and len(tweet) > 50:
                check = 0
                if dictionary[center] != None:
                    dictionary[center].append(tweet)
                else:
                    dictionary[center] = [tweet]
                break

        if check == 1:
            leftOvers.append(tweet)
    
    return dictionary, leftOvers

def pos_tweets(tweets, times, taggers):
    start_time = time.time()
    
    tagger_tweets = []
    tagger_times = []
    
    for i in range(len(tweets)):
        pos = nltk.pos_tag(word_tokenize(tweets[i]))
        unique_pos = set([single_pos for single_pos in (element[1] for element in pos) if single_pos in taggers])
        
        if len(unique_pos)>0:
            tagger_tweets.append(tweets[i])
            tagger_times.append(times[i])
    
    print("Time Taken: ", time.time()-start_time)
    
    return tagger_tweets, tagger_times

def print_clusters(dictionary):
    tweet_count = 0
    for i in dictionary:
        if dictionary[i] != None:
            print(i, " ", len(dictionary[i]))
            for value in dictionary[i]:
                tweet_count+=1
    return tweet_count

def find_specific_term(sample, term):
    return [tweet for tweet in sample if term in tweet.lower()]

def output_sample(sample):
    with open(term+ '.csv', mode='w') as f:
        output = csv.writer(f)
        output.writerow(['message'])
        for message in sample:
            output.writerow([message.encode("raw_unicode_escape")])
#             message.decode("raw_unicode_escape")
# .encode("raw_unicode_escape")