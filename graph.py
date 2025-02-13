from collections import deque
import heapq
import numpy as np
from sklearn.linear_model import LogisticRegression

class FraudDetection:
    def __init__(self):
        self.graph = {}
        self.ml_model = self.load_ml_model()

    def add_transaction(self, sender, receiver, amount):
        """ Adds transaction to graph """
        if sender not in self.graph:
            self.graph[sender] = []
        if receiver not in self.graph:
            self.graph[receiver] = []
        self.graph[sender].append((receiver, amount))
        self.graph[receiver].append((sender, amount))  

    def bfs_shortest_path(self, start):
        """ BFS implementation to find shortest suspicious paths """
        visited = {}
        queue = deque([(start, 0)])  
        visited[start] = 0
        while queue:
            node, dist = queue.popleft() 
            for neighbor, amount in self.graph[node]:
                if neighbor not in visited:
                    visited[neighbor] = dist + 1  
                    queue.append((neighbor, dist + 1))  
        return visited

    def dfs_cycle(self, node, visited, parent):
        """ Detects cycles in the graph (fraud rings) """
        visited.add(node)
        for neighbor, _ in self.graph[node]:
            if neighbor not in visited:
                if self.dfs_cycle(neighbor, visited, node):
                    return True  
            elif neighbor != parent:
                return True  
        return False

    def detect_fraud_rings(self):
        """ Detects fraud rings (cycles) in the graph """
        visited = set()
        for node in self.graph:
            if node not in visited:
                if self.dfs_cycle(node, visited, None):
                    return "⚠️ Fraud Ring Detected!"
        return "✅ No Fraud Rings Found"

    def load_ml_model(self):
        """ Load a pre-trained ML model to predict risk score """
        model = LogisticRegression()
        return model

    def train_ml_model(self, features, labels):
        """ Train ML model to predict risk score based on features """
        self.ml_model.fit(features, labels)

    def predict_risk(self, transaction):
        """ Predicts risk score for a given transaction """
        features = np.array([transaction]) 
        risk_score = self.ml_model.predict(features)  
        return risk_score[0]
