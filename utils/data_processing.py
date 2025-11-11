import pandas as pd
import os

def load_data():
    # Assuming data files are in the notebook directory
    crashes_path = '../notebook/Motor_Vehicle_Collisions_-_Crashes_20251111.csv'
    persons_path = '../notebook/Motor_Vehicle_Collisions_-_Person_20251111.csv'
    
    # Load crashes data
    df_crashes = pd.read_csv(crashes_path, low_memory=False)
    
    # Load persons data
    df_persons = pd.read_csv(persons_path, low_memory=False)
    
    # Merge on CRASH_DATE and CRASH_TIME or similar key if available
    # For simplicity, assume df_crashes has unique CRASH_DATE, but actually merge on common columns
    # Since it's collision data, perhaps merge on CRASH_DATE and LATITUDE/LONGITUDE or something
    # But to keep simple, let's assume we use df_crashes as main and add person info if needed
    # For now, return df_crashes with some processing
    
    # Convert CRASH_DATE to datetime
    df_crashes['CRASH_DATE'] = pd.to_datetime(df_crashes['CRASH_DATE'], errors='coerce')
    
    # Fill missing values or handle as needed
    df_crashes.fillna('', inplace=True)
    
    return df_crashes

def filter_data(df, borough=None, year=None, vehicle_type=None, factor=None, injury=None):
    filtered = df.copy()
    
    if borough:
        filtered = filtered[filtered['BOROUGH'].str.lower() == borough.lower()]
    
    if year:
        filtered = filtered[filtered['CRASH_DATE'].dt.year == int(year)]
    
    if vehicle_type:
        filtered = filtered[filtered['VEHICLE_TYPE'].str.lower().str.contains(vehicle_type.lower())]
    
    if factor:
        filtered = filtered[filtered['CONTRIBUTING_FACTOR'].str.lower().str.contains(factor.lower())]
    
    if injury:
        filtered = filtered[filtered['INJURY_TYPE'].str.lower().str.contains(injury.lower())]
    
    return filtered
