import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Define the API endpoint URLs
endpoints = {
    'crashes': 'https://data.cityofchicago.org/resource/85ca-t3if.json?$limit=50&$offset=500',
    'redlight': 'https://data.cityofchicago.org/resource/spqx-js37.json?$limit=50&$offset=500',
    'speed': 'https://data.cityofchicago.org/resource/hhkd-xvj4.json?$limit=50&$offset=500',
    'currrenttraffic': 'https://data.cityofchicago.org/resource/n4j6-wkkf.json?$limit=50&$offset=500'
}

# Fetch data from API endpoints and create a DataFrame
data_frames = {}
for key, url in endpoints.items():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        data_frames[key] = df
    else:
        print(f'Error fetching data from {key} endpoint.')
#print(data_frames)
# Calculate injury total per crash type
injury_per_crash = {}
for key, df in data_frames.items():
    if 'injuries_total' in df.columns and 'crash_type' in df.columns:
        df['injuries_total'] = df['injuries_total'].fillna(0).astype(int)
        #print(df['crash_type'])
        injury_per_crash[key] = df.groupby('crash_type')['injuries_total'].sum().to_dict()
    else:
        print(f'Columns not found in {key} DataFrame.')

# Print injury total per crash type
print("Injury total per crash type:")
for key, value in injury_per_crash.items():
    print(f"{key}:")
    print(value)


# Calculate primary contributory cause based on the speed limit
cause_per_speed = {}
for key, df in data_frames.items():
    if 'prim_contributory_cause' in df.columns and 'posted_speed_limit' in df.columns:
        df['posted_speed_limit'] = df['posted_speed_limit'].astype(int)
        #print(df['posted_speed_limit'])
        cause_per_speed[key] = df.groupby('prim_contributory_cause')['posted_speed_limit'].mean()
    else:
        print(f'Columns not found in {key} DataFrame.')
# Print primary contributory cause based on the speed limit
print("Primary contributory cause per posted speed limit:")
for key, value in cause_per_speed.items():
    print(f"{key}:")
    print(value)

#graph primary contributory cause based on speed limit
crash_causes = list(cause_per_speed.keys())
crash_causes = [str(crash_cause) for crash_cause in crash_causes]
speed_limit = [np.mean(list(value)) for value in cause_per_speed.values()]

plt.figure(figsize=(10, 6))
plt.bar(crash_causes, speed_limit, color='skyblue')
plt.xlabel('Primary Contributory Cause')
plt.ylabel('Average Posted Speed Limit')
plt.title('Primary Contributory Cause Based on Speed Limit')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("cause_per_speed.png")
plt.clf()


#calculate red light violations by intersection
red_light_violations_per_intersection = {}
for key, df in data_frames.items():
    if key == 'redlight' and 'intersection' in df.columns and 'violations' in df.columns:
        df['violations'] = df['violations'].astype(int)
        red_light_violations_per_intersection[key] = df.groupby('intersection')['violations'].count()
    else:
        print(f'Columns not found in {key} DataFrame.')
#print red light violations by intersection
for key, value in red_light_violations_per_intersection.items():
    print(f"{key}:")
    print(value)


#calculate number of violations per violation date
violations_per_day = {}
for key, df in data_frames.items():
    if key == 'redlight' and 'violation_date' in df.columns and 'violations' in df.columns:
        #print(df['violations'])
        df['violations'] = df['violations'].astype(int)
        violations_per_day[key] = df.groupby('violation_date')['violations'].count()
    else:
        print(f'Columns not found in {key} DataFrame.')
#print number of violations per violation date
for key, value in violations_per_day.items():
    print(f"{key}:")
    print(value)




#calculate number of violations per violation date
speed_violations_per_day = {}
for key, df in data_frames.items():
    if key == 'speed' and 'violation_date' in df.columns and 'violations' in df.columns:
        #print(df['violations'])
        df['violations'] = df['violations'].astype(int)
        speed_violations_per_day[key] = df.groupby('violation_date')['violations'].count()
    else:
        print(f'Columns not found in {key} DataFrame.')
#print number of violations per violation date
for key, value in speed_violations_per_day.items():
    print(f"{key}:")
    print(value)



# merge red light violation date with injury total
if 'crashes' in data_frames and 'redlight' in data_frames:
    merged_df1 = pd.merge(data_frames['crashes'], data_frames['redlight'], left_on='crash_date', right_on='violation_date', how='inner')
    merged_df1['injuries_total'] = merged_df1['injuries_total'].astype(int)
    injuries_per_red_date = merged_df1.groupby('violation_date')['injuries_total'].sum()
    print("Number of injuries per red light violation date:")
    print(injuries_per_red_date)
else:
    print("DataFrames 'crashes' or 'redlight' not found.")


#damage per road condition
damage_per_condition ={}
for key, value in damage_per_condition.items():
    if 'damage' in df.columns and 'weather_condition' in df.columns:
        traffic_per_street[key] = df.groupby('damage')['weather_condition'].mean()
    else:
        print(f'Columns not found in {key} DataFrame.')

#print traffic per street
for key, value in damage_per_condition.items():
    print(f"{key}:")
    print(value)

# Merge red light violations and crashes data
if 'crashes' in data_frames and 'redlight' in data_frames:
    merged_df = pd.merge(data_frames['crashes'], data_frames['redlight'], left_on='street_name', right_on='address', how='inner')
    # Perform correlation analysis
    correlation = merged_df[['violations', 'injuries_total']].corr()
    print("Correlation between Red Light Violations and Injuries:")
    print(correlation)
else:
    print("DataFrames 'crashes' or 'redlight' not found.")
# Merge speed violations and crashes data
if 'crashes' in data_frames and 'speed' in data_frames:
    merged_df = pd.merge(data_frames['crashes'], data_frames['speed'], left_on='street_name', right_on='address', how='inner')
    # Analyze crash severity based on speed violations
    crash_severity = merged_df.groupby('crash_type')['violations'].mean()
    print("Average Speed Violations per Crash Type:")
    print(crash_severity)
else:
    print("DataFrames 'crashes' or 'speed' not found.")

# Merge currrenttraffic and redlight DataFrames on 'intersection'
if 'currrenttraffic' in data_frames and 'redlight' in data_frames:
    if 'intersection' in data_frames['currrenttraffic'].columns and 'intersection' in data_frames['redlight'].columns:
        merged_df = pd.merge(data_frames['currrenttraffic'], data_frames['redlight'], on='intersection', how='inner')
        # Perform further analysis on merged data if needed
        print("Merged DataFrame:")
        print(merged_df.head())
    else:
        print("Intersection column not found in one of the DataFrames.")
else:
    print("DataFrames 'currrenttraffic' or 'redlight' not found.")

# Merge crashes data with contributory causes
if 'crashes' in data_frames:
    merged_df = data_frames['crashes']
    # Analyze primary contributory cause by crash type
    cause_per_crash_type = merged_df.groupby('crash_type')['prim_contributory_cause'].value_counts()
    print("Primary Contributory Cause per Crash Type:")
    print(cause_per_crash_type)
else:
    print("DataFrame 'crashes' not found.")


# Merge red light violations and crashes data
if 'crashes' in data_frames and 'redlight' in data_frames:
    merged_df = pd.merge(data_frames['crashes'], data_frames['redlight'], left_on='street_name', right_on='address', how='inner')
    # Create a bar chart to compare red light violations and injuries
    plt.figure(figsize=(10, 6))
    sns.barplot(data=merged_df, x='violations', y='injuries_total', hue='crash_type')
    plt.xlabel('Red Light Violations')
    plt.ylabel('Injuries Total')
    plt.title('Comparison of Red Light Violations and Injuries by Crash Type')
    #plt.legend(title='Crash Type', loc='upper right')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("red_light_vs_injuries.png")
    plt.clf()
else:
    print("DataFrames 'crashes' or 'redlight' not found.")

# Merge red light violations and crashes data for time series analysis
if 'crashes' in data_frames and 'redlight' in data_frames:
    merged_df = pd.merge(data_frames['crashes'], data_frames['redlight'], left_on='crash_date', right_on='violation_date', how='inner')
    # Convert dates to datetime objects
    merged_df['crash_date'] = pd.to_datetime(merged_df['crash_date'])
    merged_df['violation_date'] = pd.to_datetime(merged_df['violation_date'])
    # Group by date and count violations and crashes
    violations_per_day = merged_df.groupby('violation_date')['violations'].count()
    crashes_per_day = merged_df.groupby('crash_date')['crash_record_id'].count()
    # Create time series plots
    plt.figure(figsize=(10, 6))
    plt.plot(violations_per_day.index, violations_per_day.values, label='Violations', marker='o')
    plt.plot(crashes_per_day.index, crashes_per_day.values, label='Crashes', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Violations and Crashes Over Time')
    #plt.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("violations_crashes_time_series.png")
    plt.clf()
else:
    print("DataFrames 'crashes' or 'redlight' not found.")
