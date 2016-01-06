#!/usr/bin/env python
from analytics import record_forecast_data
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    db = client['homewatch']
    tab = db['forecast_data']
    tab.drop()
    record_forecast_data(tab)
