import pandas as pd

def load_data():

  df = pd.read_csv(r"Viusals\app\Components\merged_crashes_person.csv")

# optional: clean column names, parse dates, etc.

  return df

df=load_data()

Brough_options = df["BOROUGH"].dropna().unique()

CRASH_YEAR = df["CRASH_YEAR"].dropna().unique()

Contributing_Factor1 = df["CONTRIBUTING FACTOR VEHICLE 1"].dropna().unique()

Contributing_Factor2 = df["CONTRIBUTING FACTOR VEHICLE 2"].dropna().unique()

Vehicle1 = df["VEHICLE TYPE CODE 1"].dropna().unique()

Vehicle2 = df["VEHICLE TYPE CODE 2"].dropna().unique()

Injury = df["PERSON_INJURY"].dropna().unique()