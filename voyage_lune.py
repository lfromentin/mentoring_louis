import pandas as pd 

rock_samples = pd.read_csv('rocksamples.csv')

# %%
rock_samples.head()

# %%
rock_samples.info()

# %%
rock_samples['Weight (g)'] = rock_samples['Weight (g)'].apply(lambda x : x * 0.001)
rock_samples.rename(columns={'Weight (g)':'Weight (kg)'}, inplace=True)
rock_samples.head()


# %%
missions = pd.DataFrame()
missions['Mission'] = rock_samples['Mission'].unique()
missions.head()

# %%
sample_total_weight = rock_samples.groupby('Mission')['Weight (kg)'].sum()
missions = pd.merge(missions, sample_total_weight, on='Mission')
missions.rename(columns={'Weight (kg)':'Sample weight (kg)'}, inplace=True)
missions

# %%
missions['Weight diff'] = missions['Sample weight (kg)'].diff()
missions['Weight diff'] = missions['Weight diff'].fillna(value=0)

missions

# %%
missions['Lunar module (LM)'] = ['Eagle (LM-5)', 'Intrepid (LM-6)', 'Antares (LM-8)', 'Falcon (LM-10)', 'Orion (LM-11)', 'Challenger (LM-12)']
missions['LM mass (kg)'] = [15103, 15235, 15264, 16430, 16445, 16456]

# %%
missions['LM mass diff'] = missions['LM mass (kg)'].diff()
missions['LM mass diff'] = missions['LM mass diff'].fillna(0)
missions

# %%
missions['Command module (CM)'] = ['Columbia (CSM-107)', 'Yankee Clipper (CM-108)', 'Kitty Hawk (CM-110)', 'Endeavor (CM-112)', 'Casper (CM-113)', 'America (CM-114)']
missions['CM mass (kg)'] = [5560, 5609, 5758, 5875, 5840, 5960]
missions['CM mass diff'] = missions['CM mass (kg)'].diff()
missions['CM mass diff'] = missions['CM mass diff'].fillna(value=0)

# %%
missions['Total weight (kg)'] = missions['LM mass (kg)'] + missions['CM mass (kg)']
missions['Total weight diff'] = missions['LM mass diff'] + missions['CM mass diff']

# %%
saturnVPayload = 43500
missions['Crewed area : Payload'] = missions['Total weight (kg)'] / saturnVPayload
missions['Sample : Crewed area'] = missions['Sample weight (kg)'] / missions['Total weight (kg)']
missions['Sample : Payload'] = missions['Sample weight (kg)'] / saturnVPayload

# %%
crewedArea_payload_ratio = missions['Crewed area : Payload'].mean()
sample_crewedArea_ratio = missions['Sample : Crewed area'].mean()
sample_payload_ratio = missions['Sample : Payload'].mean()
print(crewedArea_payload_ratio)
print(sample_crewedArea_ratio)
print(sample_payload_ratio)

# %%
artemis_crewedArea = 26520
artemis_mission = pd.DataFrame({'Mission':['artemis1','artemis1b','artemis2'],
                                 'Total weight (kg)':[artemis_crewedArea,artemis_crewedArea,artemis_crewedArea],
                                 'Payload (kg)':[26988, 37965, 42955]})
artemis_mission['Sample weight from total (kg)'] = artemis_mission['Total weight (kg)'] * sample_crewedArea_ratio
artemis_mission['Sample weight from payload (kg)'] = artemis_mission['Payload (kg)'] * sample_payload_ratio
artemis_mission['Estimated sample weight (kg)'] = (artemis_mission['Sample weight from payload (kg)'] + artemis_mission['Sample weight from total (kg)'])/2


# %%
rock_samples['Remaining (kg)'] = rock_samples['Weight (kg)'] * (rock_samples['Pristine (%)'] * 0.01)
low_samples = rock_samples.loc[(rock_samples['Weight (kg)'] >= .16) & (rock_samples['Pristine (%)'] <= 50)]

# %%
low_samples.Type.unique()
rock_samples.Type.unique()
low_samples.groupby('Type')['Weight (kg)'].count()
needed_samples = low_samples[low_samples['Type'].isin(['Basalt', 'Breccia'])]
needed_samples.info()

# %%
needed_samples.groupby('Type')['Weight (kg)'].sum()
rock_samples.groupby('Type')['Weight (kg)'].sum()
needed_samples = pd.concat([needed_samples,rock_samples.loc[rock_samples['Type'] == 'Crustal']])
needed_samples.info()

# %%
needed_samples_overview = pd.DataFrame()
needed_samples_overview['Type'] = needed_samples.Type.unique()
needed_samples_overview

# %%
needed_sample_weights = needed_samples.groupby('Type')['Weight (kg)'].sum().reset_index()
needed_samples_overview = pd.merge(needed_samples_overview, needed_sample_weights, on='Type')
needed_samples_overview.rename(columns={'Weight (kg)':'Total weight (kg)'}, inplace=True)
needed_samples_overview

# %%
needed_sample_ave_weights = needed_samples.groupby('Type')['Weight (kg)'].mean().reset_index()
needed_samples_overview = pd.merge(needed_samples_overview, needed_sample_ave_weights, on='Type')
needed_samples_overview.rename(columns={'Weight (kg)':'Average weight (kg)'}, inplace=True)
needed_samples_overview

# %%
total_rock_count = rock_samples.groupby('Type')['ID'].count().reset_index()
needed_samples_overview = pd.merge(needed_samples_overview, total_rock_count, on='Type')
needed_samples_overview.rename(columns={'ID':'Number of samples'}, inplace=True)
total_rocks = needed_samples_overview['Number of samples'].sum()
needed_samples_overview['Percentage of rocks'] = needed_samples_overview['Number of samples'] / total_rocks
needed_samples_overview

# %%
artemis_ave_weight = artemis_mission['Estimated sample weight (kg)'].mean()
needed_samples_overview['Weight to collect'] = needed_samples_overview['Percentage of rocks'] * artemis_ave_weight
needed_samples_overview['Rocks to collect'] = needed_samples_overview['Weight to collect'] / needed_samples_overview['Average weight (kg)']
needed_samples_overview


