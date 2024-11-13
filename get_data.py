from pycampbellcr1000 import CR1000
import datetime
import pickle
import pandas as pd

device = CR1000.from_url('tcp:41.190.69.252:6785') 

def getData():
    start = datetime.datetime.now() - datetime.timedelta(days=3)
    end = datetime.datetime.now()
    weather = device.get_data('OneMin_MET', start, end)
    particulates = device.get_data('OneMin_T640', start, end)

    particulates_df = pd.DataFrame(particulates)
    print(particulates_df.head())
    weather_df = pd.DataFrame(weather)
    print(weather_df.head())
    particulates_df.set_index('Datetime')
    weather_df.set_index('Datetime')

    new_df = pd.merge(particulates_df, weather_df, on='Datetime', how='outer')
    new_df.drop_duplicates(subset='Datetime', keep='last', inplace=True)
    new_df.sort_values('Datetime', inplace=True)
    new_df.to_csv(f'dataFile-{datetime.now().date()}')

    return new_df

data = getData()

print(data.head())