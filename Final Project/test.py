import numpy as np
import pandas as dp

data = dp.read_csv("data/population.csv")

#removes repetitive columns (country or origin/asylum initials)
data = data.drop(columns = ['coo','coo_iso','coa','coa_iso'])

# Numerical data
num_data = data.drop(columns = ['coo_name','coa_name'])


# dictionary of COO:COA, returned,
year = 2010
subframe = data[data['year'] == year]   #Gets dataframe of specific year

d_coo = {}
d_coa = {}
result = []
for index, series in subframe.iterrows():
    coo = series['coo_name']
    coa = series['coa_name']
    asylum_seekers = series['asylum_seekers']
    
    # counts the number of asylum_seekers from COO to COA
    if coa not in d_coa:
        d_coa[coa] = asylum_seekers
    else:
        d_coa[coa] += asylum_seekers
    
    
    if coo not in d_coo:
        d_coo[coo] = [d_coa]
    else:
        d_coo[coo].append(d_coa)
#print(d_coo)

for key, value in d_coo.items():
    print(f"{key}: {value}")
