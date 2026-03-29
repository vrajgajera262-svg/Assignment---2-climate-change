"""
#ASSIGNMENT - 2: Statistics and Trends
#Author        : Gajera Vraj Chandubhai
#Topic         : Analysing how Climate change affect other fectures like GDP, 
                 Renewable Energy and Urban POpulation.

"""                                  

import pandas as pd                   
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

""""

#1. --- function to read worldbank file: --- #

"""

def read_worldbank(filename):


    df = pd.read_csv(filename)                                                  # Load in CSV files in python
    df.columns = df.columns.str.strip()                                         # Helps to remove emty(whitespace) from column
    year_cols = [c for c in df.columns if c.isdigit()]                          # This code keep only year columns
    df_year = df.set_index("Country Name")[year_cols]                           # Changing countries name in rows
    df_year = df_year.apply(pd.to_numeric, errors = "coerce")                   # This will convert all the values in interger numbers
    df_countries = df_year.T                                                    # It transpose years and countries into rows and columns
    df_countries.index = df_countries.index.astype(int)                         # This will convert string number to integer 
    return df_year, df_countries                                                # Return both version


""""

#2. --- Selected countries extract from files: --- #

"""

def extract(df,name):                                                           # filter dataframes to only selected countries:
    return df.loc[name]                                                         # Selecting rows as per the countries names:0


def bootstrap(data, confidence_level=0.682, nboot=1000):
    
    boot_means = []                                  
    for i in range (nboot):                                                     # repeat n_bootstrap times
        rand=np.random.choice(data, size=len(data), replace=True)               # resample with replacement
        f = function(rand)
        boot_means.append(np.mean(rand))                                        # compute and store the mean
 
    alpha = 1 - confidence_level                                                # tail probability
    low  = np.percentile(boot_means, (alpha / 2) * 100)                         # lower bound
    high = np.percentile(boot_means, (1 - alpha / 2) * 100)                     # upper bound
 
    return low, high                                                            # return the interval

""""

#3. --- Loading CSV files --- #
[y = year columns, c = countries columns]

"""

co2_y, co2_c             = read_worldbank("co2.csv")                            #  CO2 emissions 
gdp_y, gdp_c             = read_worldbank("gdp.csv")                            #  GDP per capita (USD)
renewable_y, renewable_c = read_worldbank("renewable.csv")                      #  Renewable Energy (%)
urban_y, urban_c         = read_worldbank("urban.csv")                          #  Urban POpulation (%)



""""

#4. --- Outputs of Rows from each files: --- #
# [this code mentioned helsp to ]

"""

print(co2_c.head())     
print(co2_y.head())
print(gdp_c.head())        
print(gdp_y.head())  
print(renewable_c.head())  
print(renewable_y.head())
print(urban_c.head())      
print(urban_y.head())


""""

#5. --- Understand overall data of statisical calculation: --- #

"""

print(co2_y.describe())
print(gdp_y.describe())
print(renewable_y.describe())
print(urban_y.describe())

#or

# print(co2_c.describe())
# print(gdp_c.describe())
# print(renewable_c.describe())
# print(urban_c.describe())


""""

#6. --- Selecting countries from data: --- #

"""


name = ["United Kingdom", "Afghanistan", "New Zealand", "Pakistan", "Nepal"]    # Create list of country to analyse their data

co2_ext = extract(co2_y, name)                                                  # Extract CO2 emission data for the selected country
gdp_ext = extract(gdp_y, name)                                                  # Extract GDP data for the selected country
renewable_ext = extract(renewable_y, name)                                      # Extract Renewable energy data for the selected country
urban_ext = extract(urban_y, name)                                              # Extract Urban population for the selected country

# print(co2_ext)
# print(gdp_ext)
# print(renewable_ext)
# print(urban_ext)


""""

#7. --- Calculating 3 loaded different data --- #

"""

result = pd.DataFrame(index=name)                                               # Create a DataFrame to store calculated indicators for each country
result["CO2 per GDP"]   = co2_ext["2015"]/ gdp_ext["2015"]                      # Divides CO2 emissions by GDP per capita.
result["Urban"] = urban_ext["2015"]                                             # Extract Urban Population percentage for each country (2015)
result["Renewable"] = renewable_ext["2015"]                                     # Extract Renewable Energy percentage for each country (2015)


print(result)

""""

#8. --- Applying Statistics --- #
#Mean and Statistics

"""

print("\n--- Mean and Standard Deviation (2020) ---")
print("CO2 per GDP  mean :", round(np.mean(result["CO2 per GDP"]), 6))          # average CO2 per GDP
print("CO2 per GDP  std  :", round(np.std(result["CO2 per GDP"]),  6))          # spread of values
print("Renewable %  mean :", round(np.mean(result["Renewable"]), 2))            # average renewable share
print("Renewable %  std  :", round(np.std(result["Renewable"]),  2))            # spread of values 
print("Urban %      mean :", round(np.mean(result["Urban"]), 2))                # average urban share
print("Urban %      std  :", round(np.std(result["Urban"]),  2))                # spread of values
 

""""

#9. Graph = 1: Scatter Plot (CO2 vs Renewable Energy, 2020) --- #

"""

plt.figure(figsize = (10,10))

for country in name:                                                            # loop over countries
    plt.scatter(renewable_ext.loc[country, "2020"],                             # x-axis = R0enewable Energy(%)
                co2_ext.loc[country, "2020"],                                   # y-axis = CO2(%)
                s=100)                                                          # dot size

    plt.annotate(country,                                                       # Adding label to country name on plot.
                 (renewable_ext.loc[country, "2020"],                           # x-axis = Renewable energy in 2020 of each country.
                  co2_ext.loc[country, "2020"]),                                # y-axis = CO2 Emission in 2020 of each country.
                 textcoords="offset points",                                    # Specify text for each point in graph
                 xytext=(5,5))                                                  # offset label from point

plt.xlabel("Renewable Energy Share (%, 2020)")                                  # x axis label
plt.ylabel("CO2 Emissions (Mt CO2e, 2020)")                                     # y axis label
plt.title("Renewable Energy vs CO2 Emissions (2020)")                           # chart title
plt.tight_layout()                                                              # avoid clipping
plt.show()                                                                      # display the figure


""""

#10. Graph=2 — line chart[ renewable energy % (1990-2020)]--- #

"""

years     = [str(y) for y in range(1990, 2021)]                                 # listing data from 1990 to 2020
years_int = [int(y) for y in years]                                             # coverting year into integers which we needed for x-axis while plotting 

plt.figure(figsize=(10,10))                                                          # Set figure size

for country in name:                                                            # Loop each country in dataset
    data = urban_ext.loc[country, years].astype(float).values                   # Collecting Urban Population data from selecting selected countries and years
    plt.plot(years_int, data, marker="o", label=country)                        # Each line graph labed with country name

plt.xlabel("Year")                                                              # X-axis label
plt.ylabel("Urban Population (%)")                                              # Y-axis label
plt.title("Urban Population Trend (1990-2020)")                                 # Chart title
plt.tight_layout()                                                              # Avoid clipping
plt.show()                                                                      # Plotting Graph