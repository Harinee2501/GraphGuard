import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np

features = np.array([[100, 1], [200, 2], [500, 5], [50, 1], [150, 3]])
labels = np.array([0, 1, 1, 0, 0])  

model = LogisticRegression()
model.fit(features, labels)

with open('model/fraud_model.pkl', 'wb') as f:
    pickle.dump(model, f)
