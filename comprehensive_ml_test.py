import requests
import json
import time
import numpy as np
from datetime import datetime

BASE_URL = "http://localhost:5000"

class MLBackendTester:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def print_section(self, title):
        print("\n" + "="*60)
        print(f"🔍 {title}")
        print("="*60)
    
    def log_result(self, test_name, passed, message=""):
        status = "✅ PASSED" if passed else "❌ FAILED"
        self.test_results.append({"test": test_name, "passed": passed, "message": message})
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{status}: {test_name}")
        if message:
            print(f"   📝 {message}")
    
    def test_1_health_endpoint(self):
        """Test if backend is alive and ML models are loaded"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                ml_loaded = data.get('ml_models_loaded', False)
                self.log_result(
                    "Health Check & ML Model Load Status", 
                    ml_loaded,
                    f"ML Models Loaded: {ml_loaded}"
                )
                return ml_loaded
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {e}")
            return False
    
    def test_2_prediction_accuracy(self):
        """Test if model makes correct predictions for known messages"""
        test_cases = [
            ("earthquake building collapse", "earthquake"),
            ("flood water rising rescue", "flood"),
            ("hurricane strong winds", "hurricane"),
            ("wildfire spreading fast", "wildfire"),
            ("tornado warning shelter", "tornado"),
            ("normal weather today", "normal")
        ]
        
        correct = 0
        results = []
        
        for message, expected in test_cases:
            response = requests.post(f"{BASE_URL}/predict", 
                                    json={"message": message})
            if response.status_code == 200:
                prediction = response.json().get('prediction')
                is_correct = (prediction == expected)
                if is_correct:
                    correct += 1
                results.append(f"'{message}' → {prediction} ({'✓' if is_correct else '✗'})")
            else:
                results.append(f"'{message}' → API Error")
        
        accuracy = (correct / len(test_cases)) * 100
        self.log_result(
            "Prediction Accuracy",
            accuracy >= 60,  # At least 60% accuracy for basic model
            f"Accuracy: {accuracy:.1f}% ({correct}/{len(test_cases)} correct)\n   " + "\n   ".join(results)
        )
        return accuracy
    
    def test_3_prediction_confidence(self):
        """Test if model returns confidence scores"""
        response = requests.post(f"{BASE_URL}/predict", 
                                json={"message": "earthquake disaster"})
        
        if response.status_code == 200:
            data = response.json()
            confidence = data.get('confidence')
            has_confidence = confidence is not None and 0 <= confidence <= 1
            
            self.log_result(
                "Confidence Scores",
                has_confidence,
                f"Confidence: {confidence if confidence else 'Not available'}"
            )
            return has_confidence
        else:
            self.log_result("Confidence Scores", False, "API Error")
            return False
    
    def test_4_response_time(self):
        """Test if model responds within acceptable time"""
        times = []
        for i in range(5):
            start = time.time()
            response = requests.post(f"{BASE_URL}/predict", 
                                    json={"message": f"test message {i}"})
            end = time.time()
            times.append((end - start) * 1000)  # Convert to ms
        
        avg_time = np.mean(times)
        max_time = np.max(times)
        is_fast = avg_time < 1000  # Less than 1 second
        
        self.log_result(
            "Response Time Performance",
            is_fast,
            f"Average: {avg_time:.0f}ms, Max: {max_time:.0f}ms"
        )
        return avg_time
    
    def test_5_batch_processing(self):
        """Test batch prediction endpoint"""
        batch_messages = [
            "earthquake help",
            "flood rescue needed",
            "fire emergency",
            "normal weather"
        ]
        
        response = requests.post(f"{BASE_URL}/batch-predict", 
                                json={"messages": batch_messages})
        
        if response.status_code == 200:
            data = response.json()
            predictions = data.get('predictions', [])
            total = data.get('total', 0)
            
            batch_works = len(predictions) == len(batch_messages) and total == len(batch_messages)
            
            self.log_result(
                "Batch Processing",
                batch_works,
                f"Processed {total}/{len(batch_messages)} messages"
            )
            return batch_works
        else:
            self.log_result("Batch Processing", False, f"HTTP {response.status_code}")
            return False
    
    def test_6_input_validation(self):
        """Test how API handles invalid inputs"""
        tests = [
            ("Empty message", {}),
            ("Missing message field", {"text": "wrong field"}),
            ("Empty string message", {"message": ""})
        ]
        
        all_valid = True
        for test_name, payload in tests:
            response = requests.post(f"{BASE_URL}/predict", json=payload)
            if response.status_code in [400, 422]:  # Should return bad request
                all_valid = all_valid and True
            else:
                all_valid = False
                print(f"   ⚠️  {test_name}: Expected 400, got {response.status_code}")
        
        self.log_result(
            "Input Validation",
            all_valid,
            "API correctly rejects invalid inputs"
        )
        return all_valid
    
    def test_7_model_consistency(self):
        """Test if same input always gives same prediction"""
        test_message = "earthquake shaking building"
        predictions = []
        
        for i in range(3):
            response = requests.post(f"{BASE_URL}/predict", 
                                    json={"message": test_message})
            if response.status_code == 200:
                predictions.append(response.json().get('prediction'))
            time.sleep(0.5)
        
        is_consistent = len(set(predictions)) == 1
        
        self.log_result(
            "Model Consistency",
            is_consistent,
            f"All predictions: {predictions[0] if predictions else 'None'}"
        )
        return is_consistent
    
    def test_8_different_disaster_types(self):
        """Test model can identify different disaster types"""
        disaster_types = {
            "earthquake": ["tremor", "shaking", "buildings collapse"],
            "flood": ["water rising", "inundation", "rescue boat"],
            "fire": ["wildfire", "burning", "evacuate fire"],
            "storm": ["hurricane", "cyclone", "storm winds"]
        }
        
        detected = 0
        total = 0
        
        for disaster_type, keywords in disaster_types.items():
            for keyword in keywords:
                total += 1
                response = requests.post(f"{BASE_URL}/predict", 
                                        json={"message": keyword})
                if response.status_code == 200:
                    pred = response.json().get('prediction')
                    if pred == disaster_type:
                        detected += 1
        
        diversity_score = (detected / total) * 100
        self.log_result(
            "Disaster Type Diversity",
            diversity_score > 30,  # Even basic model should catch some
            f"Detected {detected}/{total} correctly ({diversity_score:.0f}%)"
        )
        return diversity_score
    
    def run_all_tests(self):
        print("\n🚀 STARTING COMPREHENSIVE ML-BACKEND INTEGRATION TEST")
        print("="*60)
        
        # Check if backend is reachable first
        try:
            requests.get(f"{BASE_URL}/health", timeout=3)
        except:
            print("\n❌ CRITICAL: Cannot reach backend API!")
            print("   Please start the backend first: python main.py")
            print("   Then run this test again.\n")
            return False
        
        # Run all tests
        self.test_1_health_endpoint()
        self.test_2_prediction_accuracy()
        self.test_3_prediction_confidence()
        self.test_4_response_time()
        self.test_5_batch_processing()
        self.test_6_input_validation()
        self.test_7_model_consistency()
        self.test_8_different_disaster_types()
        
        # Summary
        self.print_summary()
        return self.failed == 0
    
    def print_summary(self):
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed/(self.passed+self.failed))*100:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 EXCELLENT! Your ML model is perfectly integrated with the backend!")
            print("   All systems operational and working correctly.")
        elif self.failed <= 2:
            print("\n⚠️  Good but with minor issues. Check the failed tests above.")
        else:
            print("\n❌ Multiple failures detected. Please check:")
            print("   1. Is the ML model trained? Run: python train_simple_model.py")
            print("   2. Are model files in 'models/saved/' directory?")
            print("   3. Check backend logs for errors")
            print("   4. Verify all dependencies installed")
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result["passed"] else "❌"
            print(f"   {status} {result['test']}")
            if result["message"]:
                print(f"      {result['message']}")

if __name__ == "__main__":
    tester = MLBackendTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if success else 1)
