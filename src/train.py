from model import IrisClassifier
import sys
import os

def main():
    print("🚀 Memulai training model...")
    
    # Initialize classifier
    classifier = IrisClassifier()
    
    # Fix path - cek dari berbagai lokasi yang mungkin
    possible_paths = [
        "data/sample_data.csv",           # Jika run dari root
        "../data/sample_data.csv",        # Jika run dari src/
        os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")  # Absolute path
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
    
    if data_path is None:
        print("❌ Data file tidak ditemukan!")
        print("🔍 Mencari di lokasi:")
        for path in possible_paths:
            print(f"   - {os.path.abspath(path)} {'✅' if os.path.exists(path) else '❌'}")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"📁 Directory contents: {os.listdir('.')}")
        sys.exit(1)
    
    try:
        data = classifier.load_data(data_path)
        print(f"✅ Data loaded from: {data_path}")
        print(f"✅ Data shape: {data.shape}")
        
        # Prepare data
        X_train, X_test, y_train, y_test = classifier.prepare_data(data)
        print(f"✅ Data prepared: Train={X_train.shape}, Test={X_test.shape}")
        
        # Train model
        classifier.train(X_train, y_train)
        print("✅ Model training completed!")
        
        # Evaluate
        accuracy = classifier.evaluate(X_test, y_test)
        print(f"✅ Model accuracy: {accuracy:.4f}")
        
        # Save model - PERBAIKAN: simpan di root/models/, bukan src/models/
        # Tentukan path ke root directory
        if os.path.exists("../models"):
            model_path = "../models/iris_model.pkl"
        elif os.path.exists("models"):
            model_path = "models/iris_model.pkl"
        else:
            # Buat models directory di root
            root_models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
            os.makedirs(root_models_dir, exist_ok=True)
            model_path = os.path.join(root_models_dir, "iris_model.pkl")
        
        classifier.save_model(model_path)
        print(f"✅ Model saved to: {os.path.abspath(model_path)}")
        
        # Verifikasi file tersimpan
        abs_model_path = os.path.abspath(model_path)
        if os.path.exists(abs_model_path):
            print(f"✅ Model file verified: {abs_model_path}")
            print(f"📏 Model size: {os.path.getsize(abs_model_path)} bytes")
        else:
            print(f"❌ Model file not found after saving: {abs_model_path}")
            sys.exit(1)
        
        # Quality gate: Model harus punya akurasi minimal 80%
        if accuracy < 0.8:
            print("❌ Model accuracy terlalu rendah! Deployment dibatalkan.")
            sys.exit(1)
        else:
            print("🎉 Model quality check passed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()