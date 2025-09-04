from model import IrisClassifier
import sys
import os

def main():
    print("🚀 Memulai training model...")
    
    # Initialize classifier
    classifier = IrisClassifier()
    
    # Load data
    data_path = "data/sample_data.csv"
    if not os.path.exists(data_path):
        print("❌ Data file tidak ditemukan!")
        sys.exit(1)
    
    try:
        data = classifier.load_data(data_path)
        print(f"✅ Data loaded: {data.shape}")
        
        # Prepare data
        X_train, X_test, y_train, y_test = classifier.prepare_data(data)
        print(f"✅ Data prepared: Train={X_train.shape}, Test={X_test.shape}")
        
        # Train model
        classifier.train(X_train, y_train)
        print("✅ Model training completed!")
        
        # Evaluate
        accuracy = classifier.evaluate(X_test, y_test)
        print(f"✅ Model accuracy: {accuracy:.4f}")
        
        # Save model
        model_path = "models/iris_model.pkl"
        classifier.save_model(model_path)
        print(f"✅ Model saved to: {model_path}")
        
        # Quality gate: Model harus punya akurasi minimal 80%
        if accuracy < 0.8:
            print("❌ Model accuracy terlalu rendah! Deployment dibatalkan.")
            sys.exit(1)
        else:
            print("🎉 Model quality check passed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()