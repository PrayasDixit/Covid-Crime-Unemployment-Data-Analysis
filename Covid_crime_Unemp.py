import sys
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import numpy as np
import warnings


def default_function():
    warnings.filterwarnings('ignore')
    print('-------------------------------------------------------------------------')
    print('Printing first 5 rows of Covid Data and its relevant column from API')
    s1 = 'https://data.lacity.org/resource/jsff-uc6b.json'
    content = requests.get(s1)

    x = content.json()

    covid = pd.DataFrame(x)

    covid.loc[:, 'date'] = pd.to_datetime(covid['date'])

    selected_data = covid.iloc[:, [3, 10, 11]]

    selected_data = selected_data.loc[selected_data['date'] < '2022-01-01']

    selected_data['Month'] = selected_data.date.dt.month
    selected_data['Year'] = selected_data.date.dt.year

    selected_data['new_cases'] = pd.to_numeric(selected_data['new_cases'])
    selected_data['new_deaths'] = pd.to_numeric(selected_data['new_deaths'])

    selected_data['new_cases'] = selected_data['new_cases'].abs()
    selected_data['new_deaths'] = selected_data['new_deaths'].abs()

    XC = selected_data.groupby(['Month', 'Year'], as_index=False).agg({'new_deaths': ['sum'], 'new_cases': ['sum']})

    covid_final = XC.sort_values(by=['Year', 'Month']).reset_index(drop=True)

    covid_final.columns = ['Month', 'Year', 'New_Deaths', 'New_Cases']

    covid_final.to_csv('Covid_Data.csv', index=False)
    print(covid_final.head())
    print('Dimensions of Covid data is->', covid_final.shape)

    # Scraping Data for Unemployment in LA
    print('-------------------------------------------------------------------------')
    print("Printing first 5 rows of Unemployment Data from Web Scraping")

    url = 'https://ycharts.com/indicators/los_angeles_ca_unemployment_rate'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    # response.content

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    data = soup.select(
        'body > main > div > div:nth-child(4) > div > div > div > div > div.col-md-8 > div.panel.panel-data > div.panel-content > div.row > div:nth-child(1) > table > tbody > tr')

    data2 = soup.select(
        'body > main > div > div:nth-child(4) > div > div > div > div > div.col-md-8 > div.panel.panel-data > div.panel-content > div.row > div:nth-child(2) > table > tbody > tr')

    data.extend(data2)

    l1 = []
    for d in data:
        #     print(d.td.text)
        l1.append(d.td.text)

    l2 = []
    for d in data:
        #     print(d.find('td',class_="text-right").text.strip())
        l2.append(d.find('td', class_="text-right").text.strip())

    l3 = []
    for i in l2:
        #     print(float(i[:-1]))
        l3.append(float(i[:-1]))

    df_unemp_rate = pd.DataFrame()

    df_unemp_rate['Date'] = l1
    df_unemp_rate['Unemp_Rate_(In %)'] = l3

    df_unemp_rate['Date'] = pd.to_datetime(df_unemp_rate['Date'])

    df_unemp_rate['Month'] = df_unemp_rate.Date.dt.month
    df_unemp_rate['Year'] = df_unemp_rate.Date.dt.year

    df_unemp_rate=df_unemp_rate.sort_values(['Year','Month']).reset_index(drop=True)

    df_unemp_rate=df_unemp_rate.loc[df_unemp_rate['Date']<'2022-01-01']

    df_unemp_rate = df_unemp_rate.drop('Date', axis=1)
    df_unemp_rate.to_csv('Unemp_Data.csv', index=False)
    print(df_unemp_rate.head())
    print('Dimensions of Unemployment data is->', df_unemp_rate.shape)



    # Getting Data for Crime in LA
    print('-------------------------------------------------------------------------')
    print("Printing  first 5 rows of Crime data in Los Angeles on Month Level")
    print('\n')
    print('It is quite big data therefore it may take 1-2 minutes to display')

    s2 = 'https://data.lacity.org/resource/2nrs-mtv8.json?$limit=700000'
    content2 = requests.get(s2)
    y = content2.json()
    crime = pd.DataFrame(y)

    crime['date_occ'] = pd.to_datetime(crime['date_occ'])

    crime.sort_values('date_occ', inplace=True)
    crime = crime.loc[crime['date_occ'] < '2022-01-01']

    crime['Month'] = crime.date_occ.dt.month
    crime['Year'] = crime.date_occ.dt.year

    crime_final = crime.groupby(['Month', 'Year']).size().reset_index(name='crime_count')

    crime_final = crime_final.sort_values(by=['Year', 'Month']).reset_index(drop=True)
    crime_final.to_csv('crime_data.csv', index=False)
    crime_final = crime_final[2:]
    print(crime_final.head())
    print('Dimensions of Crime data is->', crime_final.shape)

    # Plotting and Data merging will be done here
    df_unemp_rate_filtered = df_unemp_rate[df_unemp_rate['Year'] > 2019][2:]

    df_unemp_rate.Month = df_unemp_rate.Month.astype(str)
    df_unemp_rate.Year = df_unemp_rate.Year.astype(str)
    df_unemp_rate['Date'] = df_unemp_rate['Month'] + '-' + df_unemp_rate['Year']

    plt.figure(figsize=(22, 5))
    plt.xticks(rotation=45)
    plt.plot(df_unemp_rate['Date'], df_unemp_rate['Unemp_Rate_(In %)'])
    plt.xlabel('Month-Year', fontsize=18)
    plt.ylabel('Unemployment rate in %', fontsize=18)
    plt.title('Plot 1: Shift in Unemployment Rate', fontsize=18)

    plt.show()

    merged_data_2 = pd.merge(covid_final, df_unemp_rate_filtered, how='left', left_on=['Month', 'Year'],
                             right_on=['Month', 'Year'])

    merged_data_2.Month = merged_data_2.Month.astype(str)
    merged_data_2.Year = merged_data_2.Year.astype(str)
    merged_data_2['Date'] = merged_data_2['Month'] + '-' + merged_data_2['Year']

    merged_data_2 = merged_data_2.rename(columns={'Unemp_Rate_(In %)': 'Unemp_rate'})

    fig, ax1 = plt.subplots(figsize=(22, 7))

    # plot line chart on axis #1
    ax1.plot(merged_data_2['Date'], merged_data_2['Unemp_rate'])
    ax1.set_ylabel('Unemp rate in %')
    # ax1.set_ylim(0, 25)
    ax1.legend(['Unemp rate in %'], loc="upper left")

    # set up the 2nd axis
    ax2 = ax1.twinx()
    # plot bar chart on axis #2
    ax2.bar(merged_data_2['Date'], merged_data_2['New_Cases'], width=0.5, alpha=0.5, color='orange')
    ax2.grid(False)  # turn off grid #2
    ax2.set_ylabel('New cases of covid')
    # ax2.set_ylim(0, 90)
    ax2.legend(['Covid new cases'], loc="upper right")
    ax1.title.set_text('Comparing Unemployment rate with Covid cases on month level')
    ax1.set_xlabel('Date in Month and Year', fontweight='bold')
    ax1.set_xticklabels(labels=merged_data_2['Date'], rotation=45)
    plt.show()

    #Plotting Crime count vs Unemployment rate
    merged_data_3 = pd.merge(crime_final, df_unemp_rate_filtered, how='left', left_on=['Month', 'Year'],
                             right_on=['Month', 'Year'])


    merged_data_3.Month = merged_data_3.Month.astype(str)
    merged_data_3.Year = merged_data_3.Year.astype(str)
    merged_data_3['Date'] = merged_data_3['Month'] + '-' + merged_data_2['Year']

    #
    # fig, ax1 = plt.subplots(figsize=(22, 7))
    #
    # # plot line chart on axis #1
    # ax1.plot(merged_data_3['Date'], merged_data_3['Unemp_Rate_(In %)'])
    # ax1.set_ylabel('Unemp rate in %')
    # # ax1.set_ylim(0, 25)
    # ax1.legend(['Unemprate in %'], loc="upper left")
    #
    # # set up the 2nd axis
    # ax2 = ax1.twinx()
    # # plot bar chart on axis #2
    # ax2.bar(merged_data_3['Date'], merged_data_3['crime_count'], width=0.5, alpha=0.5, color='orange')
    # ax2.grid(False)  # turn off grid #2
    # ax2.set_ylabel('crime count')
    # # ax2.set_ylim(0, 90)
    # ax2.legend(['crime count'], loc="upper right")
    # ax1.title.set_text('Comparing Unemployment rate with Crime count on month level')
    # ax1.set_xlabel('Date in Month and Year', fontweight='bold')
    # plt.show()

    #Scatterplot of Crime count and Unemployment rate
    plt.scatter(merged_data_3['crime_count'], merged_data_3['Unemp_Rate_(In %)'])
    z = np.polyfit(merged_data_3['crime_count'], merged_data_3['Unemp_Rate_(In %)'], 1)
    p = np.poly1d(z)
    plt.plot(merged_data_3['crime_count'], p(merged_data_3['crime_count']), "r--")
    plt.xlabel('Crime count per month', fontweight='bold')
    plt.ylabel('Unemployment Rate in %', fontweight='bold')
    plt.show()

    #Plotting crime count per month vs New cases

    merged_data = pd.merge(covid_final, crime_final, how='left', left_on=['Month', 'Year'], right_on=['Month', 'Year'])



    merged_data.Month = merged_data.Month.astype(str)
    merged_data.Year = merged_data.Year.astype(str)


    merged_data['Date'] = merged_data['Month'] + '-' + merged_data['Year']




    fig, ax1 = plt.subplots(figsize=(22, 7))

    ax1.plot(merged_data['Date'], merged_data['crime_count'])
    ax1.set_ylabel('crime count per month')

    ax1.legend(['crime count per month'], loc="upper left")

    # set up the 2nd axis
    ax2 = ax1.twinx()

    ax2.bar(merged_data['Date'], merged_data['New_Cases'], width=0.5, alpha=0.5, color='orange')
    ax2.grid(False)  # turn off grid #2
    ax2.set_ylabel('New cases')

    ax2.legend(['New cases'], loc="upper right")
    ax1.title.set_text('Comparing Crime count with Covid cases on month level')
    ax1.set_xlabel('Date in Month and Year', fontweight='bold')
    ax1.set_xticklabels(labels=merged_data['Date'], rotation=45)
    plt.show()

    # Calculating Pearson coefficient of correlation between multiple variables
    corr = round(np.corrcoef(merged_data_3['crime_count'], merged_data_3['Unemp_Rate_(In %)'])[0, 1], 3)
    print('Pearsons correlation between Crime count and Unemployment rate: %.3f' % corr)

    corr = round(np.corrcoef(merged_data['crime_count'], merged_data['New_Cases'])[0, 1], 3)
    print('Pearsons correlation between crime count and New covid cases: %.3f' % corr)





if __name__ == '__main__':
    if len(sys.argv) == 1:
        default_function()

    # elif sys.argv[1] == '--scrape':
    #     scrape_function()

    elif sys.argv[1] == '--static':

        path_to_static_data = sys.argv[2]
        static_function(path_to_static_data)


