import joblib, json, os

def load_all_assets():
    base_path = os.path.dirname(__file__)
    models_path = os.path.join(base_path, "models")
    assets = {}
    
    folders = ["domain", "tech", "data_ai", "security", "business", "design", "writing"]
    
    for folder in folders:
        path = os.path.join(models_path, folder)
        assets[folder] = {
            "model": joblib.load(os.path.join(path, "model.pkl")),
            "le": joblib.load(os.path.join(path, "label_encoder.pkl")),
            "features": json.load(open(os.path.join(path, "features.json")))
        }
    
    explanations = json.load(open(os.path.join(base_path, "metadata", "explanations.json")))
    
    return assets, explanations