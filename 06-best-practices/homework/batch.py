#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pickle
import pandas as pd

from datetime import datetime

def get_input_path(year, month):
    # pylint: disable=line-too-long
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv("INPUT_FILE_PATTERN", default_input_pattern)
    
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    # pylint: disable=line-too-long
    default_output_pattern = 's3://nyc-duration/out/{year:04d}-{month:02d}.parquet'
    output_pattern = os.getenv("OUTPUT_FILE_PATTERN", default_output_pattern)

    if os.getenv("BATCH_TEST_RUN"):
        output_pattern = "taxi_type=fhv_year={year:04d}_month={month:02d}.parquet"

    return output_pattern.format(year=year, month=month)


def read_data(filename):
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT")
    options = {}
    if S3_ENDPOINT_URL:
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}
    return pd.read_parquet(filename, storage_options=options)

def save_data(df, filename):
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT")
    options = {}
    if S3_ENDPOINT_URL:
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}
    
    df.to_parquet(
        filename,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options,
    )

def prepare_date(df, categorical):
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def main(year, month, input_file, output_file):

    # input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # output_file = f's3://mlops-zoomcamp-rsanghvi/artifacts/model_3'

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID'] 

    df = read_data(input_file)
    df = prepare_date(df, categorical)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    save_data(df_result, output_file)

if __name__ == "__main__":

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)
    main(year, month, input_file, output_file)