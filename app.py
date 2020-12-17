from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pickle
from prediction import prediction, symp_process
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

sympfile = open('symp_list_to_send','rb')
symp_list = pickle.load(sympfile)
diction ={
    "symptoms" : symp_list
}

class symptoms_return(Resource):
    def get(self):
        return jsonify(diction)



class predict(Resource):
    def post(self):
        symptoms = request.json['symptoms']
        trainable_symptoms = []
        for i in symptoms:
            temp = symp_process(i)
            trainable_symptoms.append(temp)
        disease = prediction(trainable_symptoms)
        predicted = {"prediction" : disease}
        return jsonify(predicted)

api.add_resource(symptoms_return, "/symptoms")
api.add_resource(predict, "/predict")

if __name__ == "__main__":
    app.run(debug=True)