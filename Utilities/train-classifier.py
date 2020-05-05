# This file trains a classifier with a csv file

# This is a command-line utility that uses the following arguments (classifier_file, csv_file)

import sys
import csv
import pickle
from textblob.classifiers import NaiveBayesClassifier

arguments = sys.argv
opened_classifier = None

if len(arguments) == 1:
    print("This is a command-line utility that uses the following arguments: classifier_file, csv_file")
    raise Exception("No arguments found")

classifier_file = str(arguments[1])
csv_file = str(arguments[2])

# Opening pickled object
with open(classifier_file, 'rb') as input:
    opened_classifier = pickle.load(input)

# Checking that the opened object is a classifier instance
if type(opened_classifier) != NaiveBayesClassifier:
    raise TypeError("The file is not a classifier")

# Opening CSV
csv_data = open(csv_file, newline='', encoding='utf-8')

# Reading csv to convert to the data structure TextBlob requires 
required_structure = []
reader = csv.reader(csv_data)
item_counter = 0

for row in reader:
    item_counter += 1
    print("Converting item #{0}".format(item_counter), sep=' ', end='\r', flush=True)
    required_structure.append((row[0], row[1]))

print("\nDone converting")

# Train classifier
print("Training...")
opened_classifier.update(required_structure)

# Saving updated classifier
with open(classifier_file, 'wb') as output:
    pickle.dump(opened_classifier, output, pickle.HIGHEST_PROTOCOL)

print("Classifier trained")