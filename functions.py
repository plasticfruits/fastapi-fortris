import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# Global variables
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

def get_unemployment_data():
    """
    Connect to bls.gov/ and get the investor data
    Returns:
        - df
    """
    url = "https://www.bls.gov/web/laus/lauhsthl.htm"
    r = requests.get(url=url, headers=headers)
    
    # get data
    soup = BeautifulSoup(r.content, "html.parser")
    target_table = soup.find("table", {"id":"lauhsthl", "class":"regular"})
    
    # convert to dataframe
    df = pd.read_html(target_table.prettify())[0]
    
    # clean df
    df.columns = [c[0] + "_" + c[1] for c in df.columns] 
    return df
