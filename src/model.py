import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

class IrisClassifier:
    def __init__(self):
        self.model = LogisticRegression(random_state=42)
        self.is_trained = False
    
    def load_data(self, data_path):
        """Load data dari file CSV"""
        try:
            data = pd.read_csv(data_path)
            return data
        except Exception as e:
            raise Exception(f"Error loading data: {e}")
    
    def prepare_data(self, data):
        """Prepare data untuk training"""
        # Asumsi kolom terakhir adalah target
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train(self, X_train, y_train):
        """Train model"""
        self.model.fit(X_train, y_train)
        self.is_trained = True
        return self
    
    def evaluate(self, X_test, y_test):
        """Evaluate model"""
        if not self.is_trained:
            raise Exception("Model belum di-train!")
        
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        return accuracy
    
    def save_model(self, path):
        """Save model ke file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        return path