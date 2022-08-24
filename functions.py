import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


### Task 1 --- Life Expectancy ---
def life_expectancy_some(DF, sex, race, year):
    """
    return {"Hello": "World"}
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



### Task 4 --- Weather ---

