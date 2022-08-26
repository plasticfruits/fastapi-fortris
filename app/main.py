from fastapi import FastAPI, APIRouter
from typing import Optional
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import json
from .functions import *


# Read weather API from local file // .gitignore
""" with open("../secrets.json") as f:
    file = json.load(f)
WEATHER_API_KEY = file["key"]
f.close() """


app = FastAPI(title="Fortris API", openapi_url="/openapi.json")
api_router = APIRouter()


@app.get("/")
def read_root():
    return {"About": "This is a simple FastAPI for the fortris.com Python Developer challenge",
            "Docs & Testing": "Check the documentation at /docs",
            "With ♥ by": "@plasticfruits"}


# Task 1 --- Life Expectancy ---
@api_router.get("/life_expectancy/", status_code=200)
def search_recipes(sex: Optional[str] = None,
                   race: Optional[str] = None,
                   year: Optional[str] = None) -> dict:
    """
    Get average life expectancy for sex, race and age.
    List of possible values:
        - sex: [Male, Female, Both Sexes]
        - race: [Black, White, All Races]
        - year: [1900:2018]
    """
    # Load JSON end point
    source = 'https://data.cdc.gov/resource/w9j2-ggv5.json'
    url = requests.get(source)
    DATA = json.loads(url.text)
    DF = pd.DataFrame(DATA)
    
    # Get data
    if any(not x for x in (sex, race, year)):
        return life_expectancy_some(DF, sex, race, year)
    else:
        return life_expectancy_all(DF, sex, race, year)
          
            
# Task 2 --- Unemployment ---
@api_router.get("/unemployment/", status_code=200)
def search_recipes(state: str) -> dict:
    """
    Get unemployment rate for a given state in the USA.
    List of possible values:
        - state: [Alabama, Alaska, ..., Wyoming]
    """  
    df = fetch_unemployment_data() 
    return get_unemployment_rate(df, state)


# Task 3 --- Trends ---
@api_router.get("/trends/", status_code=200)
def search_recipes(phrase: str,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None) -> dict:
    """
    Get trends for given phrase and date range. If no date range is given,
    trends for the last 14 days are returned.
    List of possible values:
        - phrase: [any phrase] (e.g. "Day dreaming")
        - start_date: [YYYY-MM-DD] (e.g. "2021-01-01")
        - end_date: [YYYY-MM-DD] (e.g. "2021-12-31")
    """
    
    return get_google_trends(phrase, start_date, end_date)


# Task 4 --- Weather ---
@app.get("/weather/", status_code=200)
def get_weather():
    """
    Get weather history for last 7 days based on location of IP address
    List of possible values:
        - None
    """

    return get_weather_history()
    
    
# Task 5 --- Trends & Weather ---
@api_router.get("/trends_weather/", status_code=200)
async def get_trends_and_weather(phrase: str) -> dict:
    """
    Get trends and weather for given phrase in the last 7 days.
    Note: Google Trends API does not return last 3 days of data
    List of possible values:
        - Phrase: [any phrase] (e.g. "REM music band")
    """
    trends = get_google_trends(phrase)
    trends_df = pd.DataFrame(trends[phrase])
    
    # Data Wrangling
    weather = get_weather_history()
    weather_df = pd.DataFrame(pd.Series(weather).iloc[3:]).rename(columns = {0:'weather'})
    merge_df = pd.merge(weather_df, trends_df, left_index=True, right_on='date')
    merge_df = merge_df[['date', 'interest', 'weather']]
    merge_dict = merge_df.to_dict('records')

    return merge_dict
    

app.include_router(api_router)

