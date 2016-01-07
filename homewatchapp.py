from flask import Flask, request, render_template
from pymongo import MongoClient

import datetime
import json

from analytics import get_heat_pump_data, \
    get_hourly_temperature_forecast, \
    js_date_str, \
    get_outside_temp_history

from settings import password

app = Flask(__name__)


@app.route('/pump_report', methods=['POST', ])
def pump_report():
    raw = request.json
    data = json.loads(raw)

    sent_password = data.pop('password')
    data['status'] = 1
    data['datetime'] = datetime.datetime.strptime(data['timestamp'], "%Y%m%d:%H%M%S")

    if sent_password == password:
        heat_pump_table.insert_one(data)
    else:
        pass

    return ''


@app.route('/')
def index():
    try:
        heat_data = get_heat_pump_data(heat_pump_table)
    except KeyError:
        heat_data = []

    forecast_data = get_hourly_temperature_forecast(forecast_table)
    outside_temp = get_outside_temp_history(outside_table)

    return render_template('results.html',
                           heat_pump_data=heat_data,
                           forecast=forecast_data,
                           outside=outside_temp,
                           now=datetime.datetime.utcnow().strftime(js_date_str))


if __name__ == "__main__":
    client = MongoClient()
    db = client['homewatch']
    heat_pump_table = db['heat_pump']
    forecast_table = db['forecast_data']
    outside_table = db['outside_temp']

    app.run(host='0.0.0.0', port=8080, debug=False)
