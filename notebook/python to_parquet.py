import pandas as pd

# 1. Read your large CSV
print("Reading CSV...")
df = pd.read_csv("merge.csv", low_memory=False)

# 2. Convert to Parquet (Compresses file size by ~80%)
print("Converting to Parquet...")
df.to_parquet("merged_crashes.parquet", engine="pyarrow")

print("Success! Created 'merged_crashes.parquet'")