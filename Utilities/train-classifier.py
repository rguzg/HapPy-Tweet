# This file trains a classifier with a csv file

# This is a command-line utility that uses the following arguments (classifier_file, csv_file, samples)

import sys
import csv
import pickle
from textblob.classifiers import NaiveBayesClassifier

arguments = sys.argv
opened_classifier = None

if len(arguments) < 3:
    print("This is a command-line utility that uses the following arguments: classifier_file, csv_file, samples")
    raise Exception("No arguments found")

classifier_file = str(arguments[1])
csv_file = str(arguments[2])
samples = str(arguments[3])

# Opening pickled object
with open(classifier_file, 'rb') as input:
    opened_classifier = pickle.load(input)

# Checking that the opened object is a classifier instance
if type(opened_classifier) != NaiveBayesClassifier:
    raise TypeError("The file is not a classifier")

# Opening CSV
csv_data = open(csv_file, newline='', encoding='utf-8')

# Reading csv to convert to the data structure TextBlob requires 
reader = csv.reader(csv_data)
item_counter = 0

print("Training...")

for row in reader:
    # Stop execution after sample number is reached
    if item_counter == samples:
        break

    required_structure = []

    item_counter += 1
    print("Training item #{0}".format(item_counter), sep=' ', end='\r', flush=True)
    required_structure.append((row[0], row[1]))
    
    # Train classifier
    opened_classifier.update(required_structure)


# Saving updated classifier
print("Saving {0}...".format(classifier_file))
with open(classifier_file, 'wb') as output:
    pickle.dump(opened_classifier, output, pickle.HIGHEST_PROTOCOL)

print("Classifier trained")