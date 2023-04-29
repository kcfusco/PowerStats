from zipfile import ZipFile
from urllib.request import urlretrieve
import urllib.error
#import pandas as pd
#import urllib
import os
#import seaborn as sns
#import matplotlib.pyplot as plt
import shutil


def download_zip():
    """download openpowerlifting data (~77mb) and store in this .py file's directory (default path)"""
    try:
        url = 'https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip'
        filename = url.split("/")[-1]
        if not os.path.isfile(filename):
            urlretrieve(url, filename)
    except urllib.error.HTTPError:
        print('Error downloading data: bad URL')
    return filename


def summary_stats(gender, weight_class):
    """generate summary statistics - will need to present in a more user friendly way"""
    profile = None
    if gender == 'm':
        profile = male_data.loc[male_data['WeightClassKg'] == str(weight_class)]
    elif gender == 'f':
        profile = female_data.loc[female_data['WeightClassKg'] == str(weight_class)]
    profile = profile.drop(['WeightClassKg'], axis=1)
    summary = profile.describe()
    print(summary)


def mean(gender, weight_class):
    """generate a dataframe with mean lifts and total - will be compared against user's inputted lifts in a future
    update """
    profile = None
    if gender == 'm':
        profile = male_data.loc[male_data['WeightClassKg'] == str(weight_class)]
    elif gender == 'f':
        profile = female_data.loc[female_data['WeightClassKg'] == str(weight_class)]
    profile = profile.drop(['WeightClassKg'], axis=1)
    data = pd.DataFrame({'Squat': profile[['Best3SquatKg']].mean(), 'Bench': profile[['Best3BenchKg']].mean(),
                         'Deadlift': profile[['Best3DeadliftKg']].mean()})
    data = data.reset_index()
    data['Squat'] = data['Squat'].sum()
    data['Bench'] = data['Bench'].sum()
    data['Deadlift'] = data['Deadlift'].sum()
    data = data.drop(index=[1, 2], columns='index')
    return data


def plots(gender_data):
    """@param gender_data - input either male_data or female_data """
    sns.set(style="darkgrid")
    sns.relplot(x='BodyweightKg', y='TotalKg', kind='line', data=gender_data)


def name_lookup(name):
    """@param name - input lifter's name to return a table of performance throughout competition history """
    lifter_data = male_data.loc[male_data['Name'] == str(name)]
    print(lifter_data)


zip_data = download_zip()
#zf = ZipFile('openpowerlifting-latest.zip')
#shutil.unpack_archive(zip_data)
for files in os.walk(__file__):
    print(files)
"""zip_contents = zf.namelist()
df = pd.read_csv(zf.open(zip_contents[-1]),
                 usecols=['Name', 'Sex', 'Event', 'Equipment', 'Division', 'BodyweightKg', 'WeightClassKg',
                          'Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg', 'TotalKg', 'ParentFederation'],
                 dtype={'Name': 'string', 'Sex': 'category', 'Equipment': 'category', 'ParentFederation': 'string'})

ipf_sbd_raw = df.copy().loc[(df['Event'] == 'SBD') & (df['Equipment'] == 'Raw') & (df['ParentFederation'] == 'IPF')]
ipf_sbd_raw = ipf_sbd_raw.drop(['Event', 'Equipment', 'ParentFederation'], axis=1) \
    .dropna(axis=0, subset=['Division', 'Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg'])

# create and fill a dataframe column using the sum of each row in the Squat, Bench, and Deadlift columns from ipd_sbd
summed_totals = pd.DataFrame({'TotalKg': ipf_sbd_raw[['Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg']].sum(axis=1)})
ipf_sbd_raw['TotalKg'] = summed_totals

male_data = ipf_sbd_raw.loc[ipf_sbd_raw['Sex'] == 'M']
female_data = ipf_sbd_raw.loc[ipf_sbd_raw['Sex'] == 'F']

male_data = male_data.drop(['Sex'], axis=1)
female_data = female_data.drop(['Sex'], axis=1)"""
