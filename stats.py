from zipfile import ZipFile
from urllib.request import urlretrieve
from urllib import error
import pandas as pd
import urllib
import re
import os


def download_zip():
    """download openpowerlifting data (~77mb) and store in this .py file's directory (default path)"""
    try:
        url = 'https://github.com/sstangl/openpowerlifting-static/raw/gh-pages/openpowerlifting-latest.zip'
        filename = 'openpowerlifting-latest.zip'
        if not os.path.isfile(filename):
            urlretrieve(url, filename)
    except urllib.error.HTTPError:
        print('Error downloading data: bad URL')


def quick_mean(gender, weight_class):
    profile = None
    if gender == 'm':
        profile = male_data.loc[male_data['WeightClassKg'] == str(weight_class)]
    elif gender == 'f':
        profile = female_data.loc[female_data['WeightClassKg'] == str(weight_class)]
    profile = profile.drop(['WeightClassKg'], axis=1)
    mean = profile.describe()
    return mean


def name_lookup(name):
    lifter_data = male_data.loc[male_data['Name'] == str(name)]
    print(lifter_data)


download_zip()
zf = ZipFile('openpowerlifting-latest.zip')
zip_contents = zf.namelist()
df = pd.read_csv(zf.open(zip_contents[-1]),
                 usecols=['Name', 'Sex', 'Event', 'Equipment', 'Division', 'BodyweightKg', 'WeightClassKg',
                          'Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg', 'TotalKg', 'ParentFederation'],
                 dtype={'Name': 'string', 'Sex': 'category', 'Equipment': 'category', 'ParentFederation': 'string'})
# df = df.rename(columns={'Best3SquatKg': 'Squat', 'Best3BenchKg': 'Bench',
# 'Best3DeadliftKg': 'Deadlift', 'TotalKg': 'Total'})

ipf_sbd_raw = df.copy().loc[(df['Event'] == 'SBD') & (df['Equipment'] == 'Raw') & (df['ParentFederation'] == 'IPF')]
ipf_sbd_raw = ipf_sbd_raw.drop(['Event', 'Equipment', 'ParentFederation'], axis=1)
ipf_sbd_raw = ipf_sbd_raw.dropna(axis=0, subset=['Division', 'Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg'])

# create a DF from a dict. which takes each ipf_sbd_raw column name and fills
summed_totals = pd.DataFrame({'TotalKg': ipf_sbd_raw[['Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg']].sum(axis=1)})
ipf_sbd_raw['TotalKg'] = summed_totals

male_data = ipf_sbd_raw.loc[ipf_sbd_raw['Sex'] == 'M']
male_data = male_data.drop(['Sex'], axis=1)
female_data = ipf_sbd_raw.loc[ipf_sbd_raw['Sex'] == 'F']
female_data = female_data.drop(['Sex'], axis=1)




