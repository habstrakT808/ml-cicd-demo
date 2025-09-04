import pytest
import pandas as pd
import numpy as np
from src.model import IrisClassifier
import tempfile
import os

class TestIrisClassifier:
    
    def setup_method(self):
        """Setup untuk setiap test"""
        self.classifier = IrisClassifier()
        
        # Buat sample data untuk testing
        np.random.seed(42)
        self.sample_data = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'feature3': np.random.rand(100),
            'feature4': np.random.rand(100),
            'target': np.random.choice([0, 1, 2], 100)
        })
    
    def test_model_initialization(self):
        """Test apakah model bisa diinisialisasi"""
        assert self.classifier.model is not None
        assert self.classifier.is_trained == False
    
    def test_prepare_data(self):
        """Test data preparation"""
        X_train, X_test, y_train, y_test = self.classifier.prepare_data(self.sample_data)
        
        assert len(X_train) == 80  # 80% dari 100
        assert len(X_test) == 20   # 20% dari 100
        assert len(y_train) == 80
        assert len(y_test) == 20
    
    def test_model_training(self):
        """Test model training"""
        X_train, X_test, y_train, y_test = self.classifier.prepare_data(self.sample_data)
        
        # Train model
        self.classifier.train(X_train, y_train)
        
        assert self.classifier.is_trained == True
    
    def test_model_evaluation(self):
        """Test model evaluation"""
        X_train, X_test, y_train, y_test = self.classifier.prepare_data(self.sample_data)
        
        # Train dulu
        self.classifier.train(X_train, y_train)
        
        # Evaluate
        accuracy = self.classifier.evaluate(X_test, y_test)
        
        assert isinstance(accuracy, float)
        assert 0 <= accuracy <= 1
    
    def test_model_save(self):
        """Test model saving"""
        X_train, X_test, y_train, y_test = self.classifier.prepare_data(self.sample_data)
        self.classifier.train(X_train, y_train)
        
        # Save ke temporary file
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp:
            model_path = self.classifier.save_model(tmp.name)
            assert os.path.exists(model_path)
            
            # Cleanup
            os.unlink(tmp.name)