import pandas as pd

def process_match_table(df):
    # 1. drop columns
    df = df.drop(columns=["distance_units", "sightadviceaccept_shot_id", "time_prep", "time_shoot", "time_warn", "forced_end"])

    # 2. parse dates
    df['_time_c'] = pd.to_datetime(df['_time_c'], unit='s')
    df['_time_u'] = pd.to_datetime(df['_time_u'], unit='s')
    df['date'] = pd.to_datetime(df['date'], unit='s')

    # 3. map values
    type_mapping = {
        1: 'WA Outdoor',
        3: 'WA Indoor',
        0: 'Custom',
        12: 'FITA Outdoor'
    }
    competition_mapping = {
        0: 'training',
        1: 'competition',
        2: 'tuning'
    }
    face_mapping = {
        0: 'blank bale',
        10: '122cm',
        2: ''
    }
    meteo_weather_mapping = {
        0: 'sunny',
        1: 'cloudy with sun',
        2: 'cloudy',
        3: 'light rain',
        4: 'heavy rain',
        5: 'indoor',
    }
    meteo_wind_mapping = {
        0: '0bft',
        1: '1bft',
        2: '2bft',
        3: '3bft',
        4: '4bft',
        5: '5bft',
        6: '6bft',
        7: '7bft',
        8: '8bft',
        9: '9bft'
    }

    df['type'] = df['type'].replace(type_mapping)
    df['competition'] = df['competition'].replace(competition_mapping)
    df['face'] = df['face'].replace(face_mapping)
    df['meteo_weather'] = df['meteo_weather'].replace(meteo_weather_mapping)
    df['meteo_wind'] = df['meteo_wind'].replace(meteo_wind_mapping)

    return df