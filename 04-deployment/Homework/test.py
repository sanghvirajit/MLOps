import requests

ride = {
    "taxi_type": "yellow",
    "year": 2023,
    "month": 5,
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=ride)
print(response.json()) # returns 14.24