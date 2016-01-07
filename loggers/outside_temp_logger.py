#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics import record_current_outside_temperature
from analytics import record_forecast_data
from pymongo import MongoClient

if __name__ == "__main__":

    client = MongoClient()
    db = client['homewatch']
    otable = db['outside_temp']
    ftable = db['forecast_data']

    ftable.drop()

    record_current_outside_temperature(otable)
    record_forecast_data(ftable)