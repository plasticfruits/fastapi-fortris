import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from pytrends.request import TrendReq
import pandas as pd
from datetime import date, timedelta
import json


### Task 1 --- Life Expectancy ---
def life_expectancy_some(DF, sex, race, year):
    """
    """
    vars_dict = {'sex': sex, 'race': race, 'year': year}
    new_vars = []
    for i,j in vars_dict.items():
        if not vars_dict[i]:
            continue
        else:
            new_vars.append(i)
        
    if len(new_vars)==2:
        filter = DF.loc[(DF[new_vars[0]]==vars_dict[new_vars[0]]) & 
                        (DF[new_vars[1]]==vars_dict[new_vars[1]])] 
        result = pd.to_numeric(filter['average_life_expectancy']).mean()
        return {"average_life_expectancy": round(result, 2)}
    
    elif len(new_vars)==1:
        filter = DF.loc[DF[new_vars[0]]==vars_dict[new_vars[0]]]
        result = pd.to_numeric(filter['average_life_expectancy']).mean()
        return {"average_life_expectancy": round(result, 2)}
    
    elif len(new_vars)==0:
        result = pd.to_numeric(DF['average_life_expectancy']).mean()
        return {"average_life_expectancy": round(result, 2)}
    
    else:
        pass # raise error


def life_expectancy_all(DF, sex, race, year):
    """
    """
    filter = DF.loc[(DF['sex']==sex) & 
                         (DF['race']==race) & 
                         (DF['year']==year)] 
    result = pd.to_numeric(filter['average_life_expectancy']).mean()
    return {"average_life_expectancy": round(result, 2)}



### Task 2 --- Unemployment ---
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

def fetch_unemployment_data():
    """
    Connect to bls.gov/ and get the investor data
    Returns:
        - Clean df for further analysis
    TODOS:
        - drop irrelevant rows (last 2)
    """
    url = "https://www.bls.gov/web/laus/lauhsthl.htm"
    r = requests.get(url=url, headers=headers)
    
    # get data
    soup = BeautifulSoup(r.content, "html.parser")
    target_table = soup.find("table", {"id":"lauhsthl", "class":"regular"})
    
    # convert to dataframe
    df = pd.read_html(target_table.prettify())[0]
    
    # clean df columns
    col_names = ['state', 
                 'rate', 
                 'historical_high_date',
                 'historical_high_rate',
                 'historical_low_date',
                 'historical_low_rate'
                 ]
    df.columns = col_names
    return df

def get_unemployment_rate(df, state):
    """
    """
    filter = df[df['state']==state]
    result = pd.to_numeric(filter['rate'].item())
    return {"rate": round(result, 2)}


def get_all_states(df):
    """
    """
    filter = df['state'].to_list()
    return {"Possible values": filter}


### Task 3 --- Google Trends ---
def get_google_trends(phrase, start_date=None, end_date=None):
    """
    """
    phrase = [phrase]
    pytrends = TrendReq() 
     
    if not (start_date and end_date):
        # define range for last 14 days
        date_range = pd.date_range(start=date.today() - timedelta(days=14),
                                   end=str(date.today())).strftime("%Y-%m-%d").tolist()
        # get trends 
        pytrends.build_payload(phrase, cat=0, timeframe="today 1-m")
        df = pytrends.interest_over_time().reset_index()
        
        # filter by date range and clean
        df = df[df['date'].isin(date_range)].drop('isPartial',axis=1)
        df.date = df.date.dt.strftime('%Y-%m-%d')
        df.rename(columns = {phrase[0]:'interest'}, inplace = True)
        
        response = {phrase[0] : json.loads(df.to_json(orient='records'))}
        return response
    
    else:
        pytrends.build_payload(phrase, cat=0, timeframe=f'{start_date} {end_date}')
        df = pytrends.interest_over_time().reset_index().drop('isPartial',axis=1)
        
        # filter by date range and clean
        df.date = df.date.dt.strftime('%Y-%m-%d')
        df.rename(columns = {phrase[0]:'interest'}, inplace = True)
        
        response = {phrase[0] : json.loads(df.to_json(orient='records'))}
        return response


### Task 4 --- Weather ---
def get_ip():
    """
    """
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_weather_history():
    """
    """
    WEATHER_API_KEY = '0d10212baecb4addb8261304222508' # bad practice, but for the sake of the exercise
    ip = get_ip()
    
    # generate range of dates & reverse order
    date_range = pd.date_range(start=date.today() - timedelta(days=7),
                               end=str(date.today())).strftime("%Y-%m-%d").tolist()
    date_range = list(reversed(date_range))
    
    weather_all = json.loads('{}')
    counter = 0
    for i in date_range:
        params = {'key': WEATHER_API_KEY,
                  'q': ip,
                  'dt': i}
        
        response = requests.get('http://api.weatherapi.com/v1/history.xml', params=params)
        xml_data = response.content
        tree = ET.fromstring(xml_data)
        
        if counter==0:
            weather_region = {'Location': tree.find('location/name').text,
                      'Region': tree.find('location/region').text,
                      'Country': tree.find('location/country').text}
            weather_all.update(weather_region)
            counter += 1
            
        else:
            weather_data = {tree.find('forecast/forecastday/date').text : 
                {'Condition': tree.find('forecast/forecastday/day/condition/text').text,
                 'Minimum °C': tree.find('forecast/forecastday/day/mintemp_c').text,
                 'Maximum °C': tree.find('forecast/forecastday/day/maxtemp_c').text}}
            weather_all.update(weather_data)
            counter += 1
    return weather_all



### Task 5 --- Google Trends ---