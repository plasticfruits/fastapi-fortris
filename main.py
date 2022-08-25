from typing import Union
#import uvicorn
from fastapi import FastAPI, APIRouter
from typing import Optional
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import json
from functions import *

###
from bs4 import BeautifulSoup
from datetime import date, timedelta


# Vars

# Read weather API
with open("./secrets.json") as f:
    file = json.load(f)
WEATHER_API_KEY = file["key"]
f.close()


app = FastAPI(title="Fortris API", openapi_url="/openapi.json")
api_router = APIRouter()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# Task 1 --- Life Expectancy ---
@api_router.get("/life_expectancy/", status_code=200)
def search_recipes(sex: Optional[str] = None,
                   race: Optional[str] = None,
                   year: Optional[str] = None) -> dict:
    """
    Get average life expectancy for sex, race and age
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
def search_recipes(state: Optional[str] = None) -> dict:
    """
    Get average life expectancy for sex, race and age
    TODO:
    # - if no value then return list of states
    """  
    df = fetch_unemployment_data() 
    return get_unemployment_rate(df, state)


# Task 4 --- Weather ---
@app.get("/weather/")
def get_weather():
    """
    Get weather history for last 7 days based on user's IP address
    """

    return get_weather_history()
    
 

app.include_router(api_router)


""" # Debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) """
