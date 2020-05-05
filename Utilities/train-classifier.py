# This file trains a classifier with a csv file

# This is a command-line utility that uses the following arguments (classifier_file, csv_file, samples)

import sys
import csv
import pickle
import ntpath
from textblob.classifiers import NaiveBayesClassifier

arguments = sys.argv
opened_classifier = None
delete_samples = input("Would you like to delete the samples that have been used from the .csv file? (Y/N)")

# Check that all inputs are correct
if len(arguments) < 3:
    print("This is a command-line utility that uses the following arguments: classifier_file, csv_file, samples")
    raise Exception("No arguments found")

if delete_samples.upper() != 'Y' and delete_samples.upper() != 'N':
    raise Exception("Incorrect arguments. Use Y or N")

classifier_file = str(arguments[1])
csv_file = str(arguments[2])
samples = int(arguments[3])

# Opening pickled object
with open(classifier_file, 'rb') as input:
    opened_classifier = pickle.load(input)

# Checking that the opened object is a classifier instance
if type(opened_classifier) != NaiveBayesClassifier:
    raise TypeError("The file is not a classifier")

# Opening CSV
csv_data = open(csv_file, newline='', encoding='utf-8')

#  csv.reader object to convert to the data structure TextBlob requires 
reader = csv.reader(csv_data)

unused_csvfilename = "unused_{0}".format(ntpath.basename(csv_file))
unused_csvfile = open(unused_csvfilename, 'w', newline='', encoding='utf_8')
item_counter = 0

print("Training...")

for row in reader:
    item_counter += 1

    # Stop execution after sample number is reached
    if item_counter <= samples:
        required_structure = []

        print("Training using item #{0}".format(item_counter), sep=' ', end='\r', flush=True)
        required_structure.append((row[0], row[1]))
        
        # Train classifier
        opened_classifier.update(required_structure)

    # Save unused samples
    if delete_samples.upper() == 'Y' and item_counter == samples: # This is done for formatting sake
        print("\nWriting unused item #{0}".format(item_counter), sep=' ', end='\r', flush=True)
        writer = csv.writer(unused_csvfile)

    if delete_samples.upper() == 'Y' and item_counter > samples:
        print("Writing unused item #{0}".format(item_counter), sep=' ', end='\r', flush=True)
        writer = csv.writer(unused_csvfile)
        writer.writerow(row)

# Saving updated classifier
print("\nSaving {0}...".format(classifier_file))
with open(classifier_file, 'wb') as output:
    pickle.dump(opened_classifier, output, pickle.HIGHEST_PROTOCOL)

print("Classifier trained")
if delete_samples.upper() == 'Y':
    print("Unused samples saved as {0}".format(unused_csvfilename))
