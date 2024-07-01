
import lambda_function

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49653526590086726115168643440460174274152856987245740034",
                "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDE1NgogICAgfQ==",
                "approximateArrivalTimestamp": 1719868548.994
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49653526590086726115168643440460174274152856987245740034",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::058264402883:role/lambda-kinesis-role",
            "awsRegion": "eu-central-1",
            "eventSourceARN": "arn:aws:kinesis:eu-central-1:058264402883:stream/ride_events"
        }
    ]
}


result = lambda_function.lambda_handler(event, None)
print(result)
