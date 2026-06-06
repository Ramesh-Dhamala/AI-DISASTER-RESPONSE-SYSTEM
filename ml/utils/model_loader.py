# ml/utils/model_loader.py
import os
import joblib
import pickle
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """Load and manage ML models"""
    
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            current_dir = Path(__file__).resolve().parent.parent
            self.models_dir = current_dir / 'trained_models'
        else:
            self.models_dir = Path(models_dir)
        
        self.models: Dict[str, Any] = {}
        self._verify_models_directory()
    
    def _verify_models_directory(self):
        if not self.models_dir.exists():
            logger.warning(f"Models directory not found: {self.models_dir}")
            self.models_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created models directory: {self.models_dir}")
    
    def load_model(self, model_name: str, force_reload: bool = False) -> Any:
        """Load a model by name"""
        if not force_reload and model_name in self.models:
            return self.models[model_name]
        
        # Try different filename patterns
        possible_names = [
            f"{model_name}_model.pkl",
            f"{model_name}.pkl",
            f"{model_name}_model.joblib",
            f"{model_name}.joblib"
        ]
        
        model_file = None
        for name in possible_names:
            candidate = self.models_dir / name
            if candidate.exists():
                model_file = candidate
                break
        
        if model_file is None:
            # Return a dummy model for development
            logger.warning(f"Model {model_name} not found. Using dummy model.")
            return DummyModel()
        
        try:
            if model_file.suffix == '.joblib':
                model = joblib.load(model_file)
            else:
                with open(model_file, 'rb') as f:
                    model = pickle.load(f)
            
            self.models[model_name] = model
            logger.info(f"Loaded model: {model_name}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to load {model_name}: {e}")
            return DummyModel()
    
    def predict(self, model_name: str, features) -> Any:
        """Convenience method for prediction"""
        model = self.load_model(model_name)
        return model.predict(features)


class DummyModel:
    """Dummy model for when real models aren't available"""
    def predict(self, features):
        import random
        return [random.uniform(0.2, 0.8)]
    
    def predict_proba(self, features):
        import random
        return [[random.uniform(0, 1), random.uniform(0, 1)]]


_default_loader = None

def get_model_loader() -> ModelLoader:
    global _default_loader
    if _default_loader is None:
        _default_loader = ModelLoader()
    return _default_loader