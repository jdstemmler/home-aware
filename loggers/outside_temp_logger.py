#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics import record_current_outside_temperature
from pymongo import MongoClient

if __name__ == "__main__":

    client = MongoClient()
    db = client['homewatch']
    table = db['outside_temp']

    record_current_outside_temperature(table)