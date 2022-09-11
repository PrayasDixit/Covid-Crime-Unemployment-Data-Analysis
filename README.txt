

Description: For Homework 4, I have created 3 datasets ‘Covid_Data.csv’, ’crime_data.csv’ and ‘Unemp_Data.csv’. These datasets are being created when we run our python script in default mode. 


Requirements: Following requirements are needed to be satisfied to run this code:

Packages to be installed:

1. Beautiful Soup
2. pandas
3. requests
4. json
5. Warnings
6. numpy

I have also made an requirements.txt file to automaticall install all the required packages. 
Use the following command: pip install -r requirements.txt


Data Sources:

1. Lacity Covid cases from March 2020 to Present: (https://data.lacity.org/COVID-19/LA-County-COVID-Cases/jsff-uc6b/data)
Link to fetch json: 'https://data.lacity.org/resource/jsff-uc6b.json'
Using the request library I am accessing the data and converting it into the dataframe by using pandas library. It consists of around 750 rows and it is being updated on daily basis. It has various columns out of which I took the date, New_Cases, New_Deaths. After extracting the data I have converted it to month level and added two new columns Month and Year (extracting from date column) so that it helps our further analysis. Further,  I dropped the initial ‘date’ column and finally created ‘Covid_Data.csv’ file.

2. Los Angeles Unemployment Rate from 2018 to present: (https://ycharts.com/indicators/los_angeles_ca_unemployment_rate)
For this part I am scraping the datasets from the mentioned link and saving the dataset into a csv file i.e ‘Unemp_Data.csv’. This dataset consists of two columns initially which are date and Unemployment Rate percentage. After extracting it I added two more column i.e Month and Year so that all of our three datasets have 2 comon column. Once I got the month and year column I dropped the date column because it was unnecessary. So, the final dataset consist of 3 columns Month, Year and Unemployment Rate(In percentage). I have also converted the Unemplyment rate to float type so it will be easy for me to do the future analysis and plotting.

3. Crime Data from 2020 to present: (https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/data)
Link to fetch json: https://data.lacity.org/resource/2nrs-mtv8.json?$limit=700000
Finally for the last data, I am using the request library and accessing the data, converting it into the dataframe by using pandas library. It consists of around 50000 rows. I only wanted to take the number of crime happening on monthly level in LA city. Therefore, I only took the ‘date’ data and grouped it by month and counted the number of rows which gave me the number of crime happening in LA on mothly basis from January 2020. After that I cleaned the data according to the requirements and also added two more columns i.e Month and Year to the final dataset. I have created ’crime_data.csv’ file by using this API. Regarding maintainability, this code will only take the 7,00,000 rows(because I have set 7,00,000 as limit while extracting data from API), right now the dataset has around 5,00,000 
rows.

Running the code:
The code can be run in one mode: default

python3 Covid_crime_Unemp.py



Default mode: To run the code in default mode, type command - python3 Prayas_Dixit_HW5_DSCI510.py
In this mode, all three datasets will be created in csv format. The first two datasets are generating instantly and the third data which is crime_data.csv is taking around 2 mins. I have displayed first five rows of all of the three data along with its size in rows and columns. 


NOTE: During execution this site went for a scheduled maintainace for an hour. So, if it happens again for Web Scraping part then please try it after an hour or so.
https://ycharts.com/indicators/los_angeles_ca_unemployment_rate