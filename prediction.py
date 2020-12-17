import pickle
from collections import Counter


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
        temp = { "disease" : i[0], "probability" : probability}
        disease_prediction.append(temp)
    
    return disease_prediction

    infile.close
    sympfile.close
    encode_file.close

def dataArrange(symp_list,data_list):
    temp_row= [0]*len(symp_list)
    for i in symp_list:        
        for j in data_list:
            if(i == j):
                t = symp_list.index(i)
                temp_row[t] = 1
                break
    return temp_row

def symp_process(entry):
    entry = entry.lower()
    entry = entry.replace(" ","")
    return entry
