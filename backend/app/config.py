import os

# Get project root directory (3 levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Model paths
FLOOD_MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "trained_models", "flood_model.pkl")
LANDSLIDE_MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "trained_models", "landslide_model.pkl")
EARTHQUAKE_MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "trained_models", "earthquake_model.pkl")

print(f"Project Root: {PROJECT_ROOT}")
print(f"Flood model path: {FLOOD_MODEL_PATH}")