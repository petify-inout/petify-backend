from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pickle
from prediction import prediction
from data_preprocess_util import symp_process
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
api = Api(app)

sympfile = open('symp_list_to_send','rb')
symp_list = pickle.load(sympfile)
diction ={
    "symptoms" : symp_list
}

class Disease(db.Model):
    id = db.Column(db.Integer , primary_key=True )
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    symptoms = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.symptoms}')"

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