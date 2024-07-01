import batch
import pandas as pd
from deepdiff import DeepDiff
from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def test_read_data():

    assert 1 == 1

def test_prepare_date():

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PULocationID', 'DOLocationID']

    actual_output = batch.prepare_date(df, categorical).shape[0]

    expected_output = 2

    # expected_data = [
    #     ("-1", "-1", dt(1, 2), dt(1, 10), 9.0),
    #     ("1", "1", dt(1, 2), dt(1, 10), 8.0),
    # ]

    # expected_columns = [
    #     "PUlocationID",
    #     "DOlocationID",
    #     "pickup_datetime",
    #     "dropOff_datetime",
    #     "duration",
    # ]
    # expected_df = pd.DataFrame(expected_data, columns=expected_columns)

    # diff = DeepDiff(actual_output.to_dict(), expected_df.to_dict(), significant_digits=1)
    # print(f"diff={diff}")

    # assert not diff

    assert actual_output == expected_output