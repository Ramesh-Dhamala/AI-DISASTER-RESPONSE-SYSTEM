import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_prediction():
    print("\n🤖 Testing prediction endpoint...")
    test_message = {"message": "earthquake building collapse need help"}
    response = requests.post(f"{BASE_URL}/predict", json=test_message)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Prediction: {result.get('prediction')}")
        print(f"   Confidence: {result.get('confidence')}")
    else:
        print(f"   Error: {response.json()}")
    return response.status_code == 200

def test_batch():
    print("\n�� Testing batch prediction...")
    test_data = {"messages": [
        "flood waters rising",
        "wildfire evacuation",
        "normal day routine"
    ]}
    response = requests.post(f"{BASE_URL}/batch-predict", json=test_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Processed: {result.get('total')} messages")
    return response.status_code == 200

if __name__ == "__main__":
    print("="*40)
    print("BACKEND INTEGRATION TEST")
    print("="*40)
    
    try:
        test_health()
        test_prediction()
        test_batch()
        print("\n✅ Integration test completed!")
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to backend!")
        print("   Make sure the backend is running: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
