import pandas as pd 
import re
from unidecode import unidecode

def normalize_string(s):
    if pd.isna(s):
        return ""
    s = unidecode(s) 
    s = re.sub(r'[^\w]', '', s) 
    s = s.lower()
    s = s.replace("de", "") 
    s = s.replace("av", "avenue")
    s = s.replace("bd", "boulevard")
    s = s.replace("pl", "place")
    return s