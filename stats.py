from zipfile import ZipFile
from urllib.request import urlretrieve
import os
import pandas as pd
import pyinputplus as pyip

# download openpowerlifting data (~77mb) and store in this .py file's directory
url = 'https://github.com/sstangl/openpowerlifting-static/raw/gh-pages/openpowerlifting-latest.zip'
filename = 'openpowerlifting-latest.zip'
if not os.path.isfile(filename):  # checks to see if the .zip has already been downloaded
    urlretrieve(url, filename)

# open .zip archive and read the .csv, taking only certain columns of interest
zf = ZipFile(filename)
df = pd.read_csv(zf.open('openpowerlifting-2020-06-20/openpowerlifting-2020-06-20.csv'),
                 usecols=[1, 3, 9, 14, 19, 24, 25, 34])
df = df.rename(columns={'Best3SquatKg': 'Squat', 'Best3BenchKg': 'Bench',
                        'Best3DeadliftKg': 'Deadlift', 'TotalKg': 'Total'})

# filter for male and female data for raw (no wraps) and IPF affiliated meets
male_data = df.loc[(df['Sex'] == 'M') & (df['Equipment'] == 'Raw') & (df['ParentFederation'] == 'IPF')]
female_data = df.loc[(df['Sex'] == 'F') & (df['Equipment'] == 'Raw') & (df['ParentFederation'] == 'IPF')]

# possible choices for pyinputs.inputChoice
genders = ['m', 'f']
male_classes = ['53', '59', '66', '74', '83', '93', '105', '120', '120+']
female_classes = ['43', '47', '52', '57', '63', '72', '84', '84+']


def calculate_mean():
    profile = None
    print('Gender?')
    gender = pyip.inputChoice(genders)
    if gender == 'm':
        print('Weight class?')
        weight_class = pyip.inputChoice(male_classes)
        profile = male_data.loc[male_data['WeightClassKg'] == str(weight_class)]
    elif gender == 'f':
        print('Weight class?')
        weight_class = pyip.inputChoice(female_classes)
        profile = female_data.loc[female_data['WeightClassKg'] == str(weight_class)]

    units = pyip.inputYesNo('Data in Lbs?')
    if units == 'yes':
        profile = profile[['Squat', 'Bench', 'Deadlift', 'Total']] * 2.205
    elif units == 'no':
        profile = profile[['Squat', 'Bench', 'Deadlift', 'Total']]

    print(profile.mean())
