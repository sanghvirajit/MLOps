import pickle
import pandas as pd
import sys
import numpy as np
from flask import Flask, request, jsonify

def read_data(filename):
    categorical = ['PULocationID', 'DOLocationID']
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    dicts = df[categorical].to_dict(orient='records')
    return dicts

def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def predict(dv, model, dicts):
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred

app = Flask('duration-prediction')

def ride_duration_prediction(taxi_type, year, month):

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'

    data_frame = read_data(input_file)
    dv, model = load_model()
    dicts = prepare_dictionaries(data_frame)
    y_pred = predict(dv, model, dicts)

    data_frame['ride_id'] = f'{year:04d}/{month:02d}_' + data_frame.index.astype('str')

    df_result = pd.DataFrame()
    df_result['ride_id'] = data_frame['ride_id']
    df_result['predicted_duration'] = y_pred

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

    return y_pred

@app.route('/predict', methods=['POST'])
def predict_endpoint():

    ride = request.get_json()

    taxi_type = ride["taxi_type"]
    year = ride["year"]
    month = ride["month"]

    y_predicted = ride_duration_prediction(taxi_type, year, month)

    result = {
        'duration': np.mean(y_predicted)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)