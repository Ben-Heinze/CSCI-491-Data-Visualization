import numpy as np
import pandas as dp
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


def generate_asylum_dictionary(data, year):
    subframe = data[data['year'] == int(year)]  #Gets dataframe of specific year
    d_coo = {}  #Dictionary of country of origin. { CountryOfOrigin: [listOfCountryAsylums] }
    for index, series in subframe.iterrows():
        coo = series['coo_name']  # country of origin string
        coa = series['coa_name']  # country of asylum string
        asylum_seekers = series['asylum_seekers']  # number of asylum seekers from COO to COA
        d_coa = {}  #Dictionary for country of asylum  {CountryOfAsylum: numberOfAsylumSeekers }

        # counts the number of asylum_seekers from COO to COA
        if asylum_seekers > 0:
            if coa not in d_coa:  #If countryOfAsylum isnt in the dict, add it with current value.
                d_coa[coa] = asylum_seekers
            else:  # If it's in the dict, increment dict
                d_coa[coa] += asylum_seekers

            # Create a list of Dictionaries if the country of origin doesn't exist in the COO dictionary yet
            if coo not in d_coo:
                d_coo[coo] = d_coa
            else:  # add the Country of asylum to the list if the COO does exist in the coo_dictionary
                d_coo[coo].update(d_coa)
    # print results
    print('Example:\nCountryOfOrigin: \n[{asylumForAsylumSeeker1: asylumSeekerNumber} , {asylumForAsylumSeeker2: asylumSeekerNumber}, ...]\n')
    # print(d_coo)
    # for key, value in d_coo.items():
    #     print(f"{key}: \n{value}")
    return d_coo


def plot_heat_map(country, d, year):
    # Generates Data from Country
    data = generate_asylum_dictionary(d, year)
    data = data[country]

    # Load world shapefile
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[(world.name != 'Antarctica')]  # Leave off Antarctica
    # Map the data to the image
    world['data'] = world['name'].map(data)

    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    world.boundary.plot(ax=ax, linewidth=0.8)
    world.plot(column='data', cmap='plasma', ax=ax, legend=True,
               legend_kwds={'label': "Data", 'orientation': "horizontal"})
    ax.set_title(f"World Heat Map of Where Asylum Seekers Find Refuge from {country}",fontsize=14)
    plt.show()

def main():
    data = dp.read_csv("data/population.csv")
    # removes repetitive columns (country or origin/asylum initials)
    data = data.drop(columns=['coo', 'coo_iso', 'coa', 'coa_iso'])
    # Numerical data
    num_data = data.drop(columns=['coo_name', 'coa_name'])

    plot_heat_map("Afghanistan", data, 2019)


if __name__ == '__main__':
    main()
