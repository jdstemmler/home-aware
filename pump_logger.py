#!/usr/bin/env python

import requests
import json
import time
from datetime import datetime
from requests.exceptions import ConnectionError
import sys

if __name__ == "__main__":
    while 1:
        # url = "http://homewatch.jdstemmler.com:8080/pump_report"
        url = sys.argv[-1]
        data = {"timestamp": datetime.utcnow().strftime("%Y%m%d:%H%M%S"),
                "password": "cea0f15a86e33f58127ca374b7ea8d2c88995"
               }

        # logfile = '/Users/jdstemmler/Learning/Projects/home-watch/pump_logger.log'
        try:
            requests.post(url, json=json.dumps(data))
            #     with open(logfile, 'a') as f:
            #         f.write('{} success\n'.format(datetime.now()))
        except ConnectionError:
            #     with open(logfile, 'a') as f:
            #         f.write('{} failure\n'.format(datetime.now()))
            pass

        time.sleep(60)
