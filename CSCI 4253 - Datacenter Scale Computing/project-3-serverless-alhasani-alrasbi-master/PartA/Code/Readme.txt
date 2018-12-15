# How The Lambda Function Was Created

We only have one lambda function called lambda_handler. The function's name 'def lambda_handler(event, context):' was left untouched, as AWS Lambda's default function when creating a new lambda function. It is responsible for opening files with tweets, storing the text, processing it as necessary, and outputting a file with the modified tweet to the output bucket. The lambda function is triggered each time a tweet file is added to the input bucket. Below is a detailed explanation of the code that is responsible for the trigger. 

# Integration of Lambda with our project in AWS

We were able to create this lambda function in AWS's provided services. One of those services is Lambda. Lambdas are functions that can run without a server. They can be modified to engage as needed by the user. They can engage/trigger when a file is modified, added, deleted or all together. They can also engage according to the type of file needed. In our cases, we did not specify the type of files. We knew beforehand the only files that will be added to the bucket are .txt files. 

Finally, to ensure the Lambda function works correctly, we modified its role to have full access to our S3 buckets. Additionally, it has a CloudWatch access because we used the CloudWatch service for testing purposes.

# Code Explanation
When our lambda function is triggered, the first thing that it does is that it creates an S3 object which represents Amazon Simple Storage Service (S3). 

s3 = boto3.client('s3')

Then, we created a list of stop words and a regex object that we can use to process texts from tweets. 

In the case that the function is triggered (in our case, if a file is added to our S3 bucket), the if condition code block is entered, it means that the event object passed is not empty, and it reflects an actual event/trigger.

if event:

First, we will store the first element in the 'Records' of an event. This will help us access the file's name and file's content. For reference, the event object's content is mentioned in this document: https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html .

records = event["Records"][0]
filename = str(records['s3']['object']['key'])
text = fileObj["Body"].read().decode('utf-8')

Once we store the texts from a tweet, we then process it per the project's requirement. We convert the text to lowercase and split it into single words. We check if each word is a stopword, and remove numbers and symbols. Processed words then are stored in a list, which is later joined to form the finalized tweet. 

Finally, we create a new resource object that accesses the output S3 Bucket to store the final tweet in a single text file with the same filename as the input file. 

s3_a = boto3.resource('s3')
s3_a.Bucket('output-tweets').put_object(Key=filename, Body=final_tweet)
