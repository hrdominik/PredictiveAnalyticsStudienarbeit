"""
Flask API to serv Model for Prediction of Stockprice-Movement based on Headlines of Stocknews

@author DHR
"""
__develop__ = True
# Export the sklearn Model in the Notebook to import it here
# # from sklearn.externals import joblib
# # joblib.dump(model, 'model.pkl')
# # model = joblib.load('model.pkl')

from flask import Flask, abort, request
from flask import Flask, jsonify
import pandas as pd
# from sklearn.externals import joblib
import joblib
import preProcessing
import os


# The Flask Server
app = Flask(__name__)

#Custom Error Handling
@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(errorMsg=str(e)), 400

# The Endpoints
# Endpoint with short API description
@app.route('/', methods=['GET'])
@app.route('/predict', methods=['GET'])
def home():
    return "<h1>Aktienpreis-Vorhersage</h1>"+ apiSTATUS  +"<p>Erreichen Sie die API durch einen HTTP-POST auf <b>/predict</b> um eine Vorhersage der Aktienpreisentwicklung auf Grundlage der übergebenen Überschrift einer Aktiennews zu erhalten.</p><br/>Übergeben Sie die Headline per <code>POST, application/json</code> in folgender Form: <br> <code>{<br/>'headlines': ['Dies ist eine Headline.', 'Dies ist noch eine Headline!']<br/>}</code><br/><br/>Die Antwort erfolgt ebenfalls per JSON in folgender Form: <br/> <code>{<br/>'prediction': [-0.627, 0.9983], <br/>'stockChange': [-1, 1] <br/>}</code>"

# Endpoint to Predict
@app.route('/predict', methods=['POST'])
def predict():
    # try if headlines are presented correctly
    # try:
    json_ = request.get_json()
    query = preProcessing.preProcessing(json_['headlines'], feature_list, vectorizer)
    # except:
    #     abort(400, description="No Headline presented to use for Prediction")

    # predict
    prediction = []
    for q in query:
        prediction.append(model.predict(q)[0])
    binaryPrediction = preProcessing.binaryPrediction(prediction)
    print(type(prediction))
    print(type(binaryPrediction))
    # Response
    return jsonify({'prediction': prediction, 'stockChange': binaryPrediction})

if __develop__:
    # local deployment
    if __name__ == '__main__':
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            model = joblib.load(dir_path+'\\tfidf_model.pkl')
            vectorizer = joblib.load(dir_path+'\\tfidf_vectorizer.pkl')
            feature_list = list(pd.read_csv(dir_path+'\\tfidf_features.csv')['0'])
            apiSTATUS = "<h3 style='color: green;'>API ready</h3>"
        except:
            apiSTATUS = "<h3 style='color: red;'>API not responsible</h3>"
        app.run(port=80)
# Docker deployment
try:
    model = joblib.load('./tfidf-model.pkl')
    vectorizer = joblib.load('./tfidf_vectorizer.pkl')
    feature_list = list(pd.read_csv('./tfidf_features.csv')['0'])
    apiSTATUS = "<h3 style='color: green;'>API ready</h3>"
except:
    apiSTATUS = "<h3 style='color: red;'>API not responsible</h3>"


