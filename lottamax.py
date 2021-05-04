# -*- coding: utf-8 -*-
# Scraping lotta max numbers from  https://www.lottomaxnumbers.com/past-numbers
# From scrap search by date

def get_lottoMax():
  import requests
  from bs4 import BeautifulSoup
  import re
  import pandas as pd 
  import numpy as np

  years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
  for year in years:
    url = 'https://www.lottomaxnumbers.com/numbers/' + str(year)

    # Request url
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    results = soup.find('table', {'id': 'archive-table'})
    rows = results.findAll('tr')

    table_dates = []
    for row in rows:
      dates = row.find('a', {'class': 'archive-date-link'})
      if dates is None:
          continue 
      else:
        table_dates.append(dates.text)
    #print(table_dates)

    table_numbers = []
    for row in rows:
      #print(row)
      content = row.find('ul')
      if content is None:
          continue 
      else:
        string = content.text.strip()
        string =  string.replace('\n', ' ').split()
        table_numbers.append(string)
    
    #print(table_numbers)

    together = []
    n = 0 
    for i in table_numbers:
      i.insert(0, table_dates[n])
      n += 1
      together.append(i)

    if year == 2009: 
      df = pd.DataFrame(table_numbers, columns=['Date', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Bonus'])
    else:
      temp = pd.DataFrame(table_numbers, columns=['Date', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Bonus'])  
      df = df.append(temp)

  return df

def search_date(dataframe, year:int):
  dataframe[['Month','Day','Year']] = dataframe.Date.str.split(' ', expand=True)
  dataframe.Year = dataframe.Year.astype(int)
  dataframe = dataframe.loc[dataframe['Year'] == year]

  months_list = dataframe['Month'].tolist()
  months_list = list(dict.fromkeys(months_list))
  print('These are the months you can pick from: ', months_list)
  
  month = int(input('Enter month number: '))
  months = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', 
            '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}
  month = months.get(f'{month}')

  dataframe = dataframe.loc[dataframe['Month'] == month]

  days_list = dataframe['Day'].tolist()
  print('These are the months you can pick from: ', days_list)
  day = int(input('Enter day: '))

  date = month + ' ' + str(day) + ' ' + str(year)
  dataframe = dataframe.loc[dataframe['Date'] == date]
  print(dataframe)
  return dataframe

def main():
  print('Getting lotto max data...')
  df = get_lottoMax()
  print('Lotto max data retrieved.')
  answer = input('Do you want to view dataframe or search dataframe? (view/search): ')
  if answer == 'view':
    print(df)
    return df
  elif answer == 'search':
    #Search date (format = Month day year)
    year = int(input('Enter year: '))

    # Call function based on inputs
    df = search_date(df, year)

  else:
    print('Invalid entry.')

if __name__ == '__main__':
  df = main()

