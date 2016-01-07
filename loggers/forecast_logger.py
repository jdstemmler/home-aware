#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics import record_forecast_data
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    db = client['homewatch']
    tab = db['forecast_data']
    tab.drop()
    record_forecast_data(tab)
