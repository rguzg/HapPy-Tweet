# This file creates a new classifier with some basic training data, saving it as a pickled object

# This is a command-line utility that uses the following arguments (output_name)

import sys
import pickle
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

arguments = sys.argv

if len(arguments) < 2:
    print("This is a command-line utility that uses the following arguments: output_name")
    raise Exception("No arguments found")

output_name = str(arguments[1])

train = [
    ('I love this sandwich.', 'pos'),
    ('this is an amazing place!', 'pos'),
    ('I feel very good about these beers.', 'pos'),
    ('this is my best work.', 'pos'),
    ("what an awesome view", 'pos'),
    ('I do not like this restaurant', 'neg'),
    ('I am tired of this stuff.', 'neg'),
    ("I can't deal with this", 'neg'),
    ('he is my sworn enemy!', 'neg'),
    ('my boss is horrible.', 'neg')
]

new_classifier = NaiveBayesClassifier(train, output='csv')

save_object(new_classifier, '{0}.pkl'.format(output_name))

print("Blank classifier created")
