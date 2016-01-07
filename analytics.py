import pandas as pd
import forecastio
import datetime

from settings import forecastio_key, lat, lng


js_date_str = '%Y-%m-%dT%H:%M:%S'


def __init__():
    pass


def map_datetime(dtimes):
    return map(lambda x: x.strftime(js_date_str), dtimes)


def get_forecast_data():
    forecast = forecastio.load_forecast(forecastio_key, lat, lng)
    return forecast


def record_current_outside_temperature(table):
    f = get_forecast_data()
    current = f.currently()
    record = {'current_time': current.time,
              'current_temp': current.temperature,}

    table.insert_one(record)


def record_forecast_data(table):

    f = get_forecast_data()
    hourly = f.hourly()

    points = [{'current_time': f.currently().time,
               'forecast_time': point.time,
               'temperature': point.temperature,
               'chance_precip': float(point.precipProbability)}
              for point in hourly.data]

    for point in points:
        table.insert_one(point)


def get_hourly_temperature_forecast(table):

    # f = table.find({'current_time': {'$gt': datetime.datetime.utcnow() - datetime.timedelta(hours=1)}})
    f = table.find({})
    points = [(point['forecast_time'].strftime(js_date_str), point['temperature']) for point in f]

    return points


def get_outside_temp_history(table):
    results = table.find()
    points = [(result['current_time'].strftime(js_date_str), result['current_temp']) for result in results]

    return points


def get_heat_pump_data(table):

    result = table.find({}, {'datetime': 1, 'status': 1, '_id': 0})
    df = pd.DataFrame(list(result))
    df.set_index('datetime', inplace=True)
    df = df.append(pd.DataFrame({'status': 0}, index=[datetime.datetime.utcnow()]))
    df_out = df.resample('1Min', how='max').fillna(0).astype(int)
    labels, data = df_out.index, df_out.status
    label_strings = map_datetime(labels.to_pydatetime())

    return zip(label_strings, data.tolist())
