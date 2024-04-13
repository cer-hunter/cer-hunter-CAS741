import numpy as np
import json
import sys
sys.path.insert(0, "../OAR-CAS741/")
from src.oarUtils import predictSigmoid

LABEL_NUM = 26  # Number of labels
LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
EPSILON = 0.1   # Cutoff for accuracy of predictions


def classify(inputImg):

    # Retrieve OAR Model from record
    record = open('src/model.json', 'r')
    model = json.load(record)

    if (len(model) != 0):
        weights = np.asarray(model["weights"])
        bias = np.asarray(model["bias"])
    else:
        print("No classification model found")
        return "N/A", 0

    prediction = np.empty(LABEL_NUM)
    for i in range(LABEL_NUM):
        w = weights[0, i]
        b = bias[i]
        yHat = predictSigmoid(inputImg, w, b)
        prediction[i] = yHat
    bestLbl = np.argmax(prediction)  # Finds the index of the best prediction
    # Check if predicition is above cutoff
    if prediction[bestLbl] > EPSILON:
        probability = prediction[bestLbl]
        label = "THE LETTER " + LABELS[bestLbl]
    # Otherwise confidence prediction is not identifiable is 100%
    else:
        probability = 1 - prediction[bestLbl]
        label = "NOT CLASSIFIED"

    return label, probability