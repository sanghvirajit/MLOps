import os
import pickle

import mlflow
from flask import Flask, request, jsonify

from mlflow.tracking import MlflowClient

#RUN_ID = "e25c5b7b54ff40fa81d52cdde995cea6"
#export RUN_ID="e25c5b7b54ff40fa81d52cdde995cea6"
RUN_ID = os.getenv('RUN_ID')
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("green-taxi-duration")

# Model
logged_model = f'runs:/{RUN_ID}/model'

# If artifacts are stored in s3 bucket
#logged_model = f's3://mlflow-models-alexey/1/{RUN_ID}/artifacts/model'

model = mlflow.pyfunc.load_model(logged_model)

# # dict vectorizer
# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
# path = client.download_artifacts(run_id=RUN_ID, path="dict_vectorize.bin")

# with open(path, 'rb') as f_out:
#     dv = pickle.load(f_out)

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    #X = dv.transform(features)
    preds = model.predict(features)
    return float(preds[0])


app = Flask('duration-prediction')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    features = prepare_features(ride)
    pred = predict(features)

    result = {
        'duration': pred,
        'model_version': RUN_ID
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
