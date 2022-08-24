from typing import Union
#import uvicorn
from fastapi import FastAPI, APIRouter
from typing import Optional
from varname import nameof
import pandas as pd
import numpy as np
import requests
import json


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


# Load JSON end point
source = 'https://data.cdc.gov/resource/w9j2-ggv5.json'
url = requests.get(source)
DATA = json.loads(url.text)
DATA_DF = pd.DataFrame(DATA)

    
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
    if any(not x for x in (sex, race, year)):

        vars_dict = {'sex': sex, 'race': race, 'year': year}
        new_vars = []
        for i,j in vars_dict.items():
            if not vars_dict[i]:
                continue
            else:
                new_vars.append(i)
        
        if len(new_vars)==2:
            filter = DATA_DF.loc[(DATA_DF[new_vars[0]]==vars_dict[new_vars[0]]) & 
                                 (DATA_DF[new_vars[1]]==vars_dict[new_vars[1]])] 
            result = pd.to_numeric(filter['average_life_expectancy']).mean()
            return {"average_life_expectancy": round(result, 2)}
        
        elif len(new_vars)==1:
            filter = DATA_DF.loc[DATA_DF[new_vars[0]]==vars_dict[new_vars[0]]]
            result = pd.to_numeric(filter['average_life_expectancy']).mean()
            return {"average_life_expectancy": round(result, 2)}
        
        elif len(new_vars)==0:
            result = pd.to_numeric(DATA_DF['average_life_expectancy']).mean()
            return {"average_life_expectancy": round(result, 2)}
        
        else:
            pass # raise error
        
    else:
        filter = DATA_DF.loc[(DATA_DF['sex']==sex) & 
                             (DATA_DF['race']==race) & 
                             (DATA_DF['year']==year)] 
        result = pd.to_numeric(filter['average_life_expectancy']).mean()
        return {"average_life_expectancy": round(result, 2)}
            
    
    
    


app.include_router(api_router)


""" # Debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) """