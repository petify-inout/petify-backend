from flask import jsonify, request
from flask_restful import Resource
import pickle
from petapp.prediction import prediction
from petapp.data_preprocess_util import symp_process
from petapp import api, db
from petapp.models_db import Disease 


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

class get_description(Resource):
    def get(self, id):
        disease = Disease.query.get(id)
        description = {
            "Name" : disease.name,
            "Symptoms" : disease.symptoms,
            "Description" : disease.description
        }   
        return jsonify(description)

api.add_resource(symptoms_return, "/symptoms")
api.add_resource(predict, "/predict")
api.add_resource(get_description, "/description/<int:id>")