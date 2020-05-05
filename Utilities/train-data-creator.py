# This file converts a csv file into the appropiate format for training TextBlob classifiers

# This is a command-line utility that uses the following arguments(csv_file_path text_column sentiment_column shorten encoding)

# Format is a boolean value that specifies wheter or not to format the sentiments column to the format TextBlob uses: Positive -> pos. Using format will ignore all data that doesn't have positive or negative as its sentiment.

#TODO: not limit formatting sentiments to 'positive' and 'negative'

import csv
import sys

def shorten_sentiment(sentiment):
    if sentiment.lower() == "positive":
        return "pos"
    if sentiment.lower() == "negative":
        return "neg"

arguments = sys.argv

if len(arguments) < 5:
    print("This is a command-line utility that uses the following arguments: csv_file_path, text_column, sentiment_column, shorten (true/false), encoding")
    raise Exception("Correct arguments not found")

csv_file_path = str(arguments[1])
text_column = str(arguments[2])
sentiment_column = str(arguments[3])
shorten = True if arguments[4] == 'true' else False
encoding = arguments[5]

print("Using: {0}. Text column is: {1}. Sentiment Column is: {2}. Shortening is set to: {3}. Using the following encoding: {4}".format(csv_file_path, text_column, sentiment_column, shorten, encoding))

output_file = open('outputfile.csv', newline='', mode='w', encoding='utf-8')

with open(csv_file_path, newline='', encoding=encoding) as csvfile:
    reader = csv.DictReader(csvfile)
    writer = csv.writer(output_file)

    if(shorten):
        for row in reader:
            if row[sentiment_column] == 'positive' or row[sentiment_column] == 'negative':
                writer.writerow([row[text_column], shorten_sentiment(row[sentiment_column])])
                print("Wrote: {0},{1}".format(row[text_column], shorten_sentiment(row[sentiment_column])))
    else:
        for row in reader:
            writer.writerow([row[text_column], row[sentiment_column]])
            print("Wrote: {0},{1}".format(row[text_column], row[sentiment_column]))

    print("Done")

