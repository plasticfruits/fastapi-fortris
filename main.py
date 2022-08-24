from typing import Union
#import uvicorn
from fastapi import FastAPI, APIRouter
from typing import Optional
from varname import nameof
import pandas as pd
import numpy as np
import requests
import json
from functions import *



TEST = [{'year': '1900',
  'race': 'Black',
  'sex': 'Male',
  'average_life_expectancy': '47.3',
  'mortality': '2518.0'},
 {'year': '1901',
  'race': 'All Races',
  'sex': 'Both Sexes',
  'average_life_expectancy': '49.1',
  'mortality': '2473.1'},
 {'year': '1902',
  'race': 'Black',
  'sex': 'Female',
  'average_life_expectancy': '51.5',
  'mortality': '2301.3'}]

app = FastAPI(title="Fortris API", openapi_url="/openapi.json")
api_router = APIRouter()


    
@app.get("/")
def read_root():
    return {"Hello": "World"}


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
            
    
@api_router.get("/unemployment/", status_code=200)
def search_recipes(state: Optional[str] = None) -> dict:
    """
    Get average life expectancy for sex, race and age
    TODO:
    # - if no value then return list of states
    """  
    df = fetch_unemployment_data() 
    return get_unemployment_rate(df, state)


app.include_router(api_router)


""" # Debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) """
