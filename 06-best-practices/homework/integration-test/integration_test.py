import pandas as pd
from datetime import datetime
import os

year = 2023
month = 1

input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f's3://nyc-duration/in/{year:04d}-{month:02d}.parquet'

# aws localstack interation commands
# aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
# aws --endpoint-url=http://localhost:4566 s3 ls  
# aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration/ --recursive
# aws --endpoint-url=http://localhost:4566 s3 rm s3://nyc-duration/ --recursive

options = {
    'client_kwargs': {
        'endpoint_url': "http://localhost:4566"
    }
}

def read_data(filename):
    
    df = pd.read_parquet(filename)

    return df

def prepare_date(df, categorical):
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)

df.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

# ################## Batch run
os.system(f"cd .. && python batch.py {year:04d} {month:02d}")

################## Uploaded data verification
df = pd.read_parquet(
    f"s3://nyc-duration/out/{year:04d}-{month:02d}.parquet", storage_options=options
)
print(df)
total_duration = (df["predicted_duration"]).sum()
print(f"Total duration: {total_duration}")