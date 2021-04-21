import pickle
from collections import Counter
from petapp.data_preprocess_util import dataArrange
from petapp import decision_tree_scratch, db
from petapp.models_db import Disease

def prediction(X_raw):
    sympfile = open('symp_model','rb')
    symp_list = pickle.load(sympfile)

    infile = open('model','rb')
    clf = pickle.load(infile)

    encode_file = open('encode_model','rb')
    encode = pickle.load(encode_file)

    X = dataArrange(symp_list , X_raw)
    X = [X]

    pred_array = []
    for count in range(10):
        pred = (clf[count].predict(X))
        pred = encode.inverse_transform(pred)
        pred_array.append(pred[0])
    

    counter = Counter(pred_array)
    iterator = counter.most_common()

    disease_prediction = []

    for i in iterator:
      
        probability = i[1]
        probability/=10
        probability *= 100
        disease = Disease.query.filter_by(name=i[0]).first()
        temp = { "disease" : disease.name,"id" : disease.id, "probability" : probability}
        disease_prediction.append(temp)
    
    return disease_prediction

    infile.close
    sympfile.close
    encode_file.close

