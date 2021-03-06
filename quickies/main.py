"""
main.py
    Our initial attempt at a working model. 
    Was used during development to understand how various libaries work.
    Not in use in the final application.
"""

import sys
#try: 
import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
from collections import Counter

from transform import add_vic_coordinates
from filter_columns import filter_columns
from balance import balance
from vector import ProcessPoints
from add_env_data import add_columns

def main(fname):
    dataset = pd.read_csv(fname)#.sort_values(by='is_reliable')

    data = filter_columns(dataset)
    balanced_data = balance(data)
    print("random", Counter(balanced_data['random'][1]))
    print("smote", Counter(balanced_data['smote'][1]))
    print("adasyn", Counter(balanced_data['adasyn'][1]))

    x, y = balanced_data['smote']
    x = add_vic_coordinates(x)
    print(x)
    x = add_columns(x)
    #x[['latitude', 'longitude']] = scale(x[['latitude', 'longitude']])
    print(x)
    scaled = pd.DataFrame(scale(x), index=x.index, columns=x.columns)
    scaled['vic_x'] = x['vic_x']
    scaled['vic_y'] = x['vic_y']
    x = scaled
    print(x)
    

    for f in ['../raw_dataset/VMLITE/VMLITE_BUILT_UP_AREA.shp', '../raw_dataset/VMLITE/VMLITE_FOREST_SU2.shp',
        '../raw_dataset/VMLITE/VMLITE_HY_WATER_AREA.shp', '../raw_dataset/VMLITE/VMLITE_PUBLIC_LAND_SU3.shp']:
        print(f)
        x = ProcessPoints(x, f)

    print(x)
    x = x.drop(columns=['vic_x', 'vic_y'])
    print(x)
    
    
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 0.1)

    md = svm.SVC(gamma='scale')
    md.fit(xTrain, yTrain)

    predictions = md.predict(xTest)

    accuracy = accuracy_score(yTest, predictions)
    print(accuracy)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} [filename]\n\nFilename: path to filtered and preprocessed csv file".format(sys.argv[0]))
        sys.exit(1)
    else: main(sys.argv[1])