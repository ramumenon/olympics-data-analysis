# --------------
#Importing header files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Path of the file is stored in the variable path

#Code starts here

# Data Loading 
data = pd.read_csv(path)
data.rename(columns = {'Total': 'Total_Medals'}, inplace = True)
data.head(10)
data.tail(10)
data.drop(index = 146, axis = 0, inplace = True)
# Summer or Winter
data["Better_Event"] = np.where(data['Total_Summer'] >= data['Total_Winter'], 'Summer', np.where(data["Total_Summer"] < data['Total_Winter'], 'Winter', 'Both'))

#remove last row wchich is a table total


# Top 10
better_event = data.Better_Event.value_counts().nlargest(1).index[0]


# Plotting top 10
def top_ten (df, col) :
    return df.nlargest(10, col)['Country_Name'].tolist()

# Top Performing Countries
top_10_summer = top_ten(data, 'Total_Summer')
top_10_winter = top_ten(data, 'Total_Winter')
top_10 = top_ten(data, 'Total_Medals')

# Best in the world 
common = list(set(top_10).intersection(top_10_summer, top_10_winter))
print(common)

summer_df = data[data.Country_Name.isin (top_10_summer)]
winter_df = data[data.Country_Name.isin (top_10_winter)]
top_df =data[data.Country_Name.isin (top_10)]

# Plotting the best
def plot_medals (df, season, colour) :
    
    plt.figure (figsize = (15,10))
    plt.barh('Country_Name', 'Total_Medals', data = df.sort_values('Total_Medals', ascending = True) , color = colour,
              edgecolor = 'k' ,linewidth = 1)
    plt.title ('Top 10 ' + season + ' games medal Tally')
    plt.xlabel ('Country')
    plt.ylabel('Number of Medals')
    plt.show()

plot_medals (summer_df, 'Summer', 'r')
plot_medals (winter_df, 'Winter', 'b')
plot_medals (top_df,    'Overall', 'y')

summer_df["Golden_Ratio"] = summer_df['Gold_Summer']/summer_df['Total_Summer']
summer_country_gold, summer_max_ratio = (summer_df.loc[summer_df.Golden_Ratio == max(summer_df.Golden_Ratio)]).iloc[0][['Country_Name','Golden_Ratio']]

winter_df["Golden_Ratio"] = winter_df['Gold_Winter']/winter_df['Total_Winter']
winter_country_gold, winter_max_ratio = (winter_df.loc[winter_df.Golden_Ratio == max(winter_df.Golden_Ratio)]).iloc[0][['Country_Name','Golden_Ratio']]

top_df["Golden_Ratio"] = top_df['Gold_Total']/top_df['Total_Medals']
top_country_gold, top_max_ratio = (top_df.loc[top_df.Golden_Ratio == max(top_df.Golden_Ratio)]).iloc[0][['Country_Name','Golden_Ratio']]


data1 = data.copy()
data1['Total_Points'] = (data1['Gold_Total'] * 3 + data1['Silver_Total'] * 2 + data1['Bronze_Total'])
most_points, best_country = (data1.loc[data1.Total_Points == max(data1.Total_Points)]).iloc[0][['Total_Points', 'Country_Name']]

best = data.loc[data['Country_Name'] == best_country][['Gold_Total','Silver_Total','Bronze_Total']]

best.plot.bar(stacked = True, figsize = (15,10))
plt.xlabel (best_country)
plt.ylabel ('Medal Tally - Stacked')
plt.xticks (rotation = 45)
plt.show()



