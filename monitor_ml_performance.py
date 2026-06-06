import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def monitor_ml_model():
    """Continuously monitor ML model performance"""
    print("📊 Starting Real-time ML Model Monitor (Press Ctrl+C to stop)")
    print("="*60)
    
    test_messages = [
        "earthquake building collapse",
        "flood water rising",
        "hurricane warning",
        "wildfire evacuation",
        "tornado alert"
    ]
    
    stats = {
        "total_requests": 0,
        "successful": 0,
        "failed": 0,
        "avg_response_time": 0,
        "predictions": {}
    }
    
    try:
        while True:
            for msg in test_messages:
                start_time = time.time()
                
                try:
                    response = requests.post(f"{BASE_URL}/predict", 
                                           json={"message": msg},
                                           timeout=5)
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1000
                    
                    stats["total_requests"] += 1
                    
                    if response.status_code == 200:
                        stats["successful"] += 1
                        data = response.json()
                        prediction = data.get('prediction')
                        
                        # Track prediction frequencies
                        stats["predictions"][prediction] = stats["predictions"].get(prediction, 0) + 1
                        
                        # Update average response time
                        stats["avg_response_time"] = (
                            (stats["avg_response_time"] * (stats["successful"] - 1) + response_time) 
                            / stats["successful"]
                        )
                        
                        # Display real-time result
                        print(f"\r[{datetime.now().strftime('%H:%M:%S')}] "
                              f"📨 '{msg[:20]}...' → {prediction} "
                              f"⚡ {response_time:.0f}ms", end="")
                        
                    else:
                        stats["failed"] += 1
                        print(f"\n❌ Failed: {msg} - HTTP {response.status_code}")
                        
                except Exception as e:
                    stats["failed"] += 1
                    print(f"\n❌ Error: {msg} - {str(e)[:50]}")
                
                time.sleep(2)  # Wait between requests
            
            # Display stats every cycle
            print("\n" + "="*60)
            print(f"📈 Stats: Success={stats['successful']}, "
                  f"Failed={stats['failed']}, "
                  f"Avg Response={stats['avg_response_time']:.0f}ms")
            print(f"🎯 Predictions: {stats['predictions']}")
            print("="*60)
            
    except KeyboardInterrupt:
        print("\n\n📊 Final Statistics:")
        print(json.dumps(stats, indent=2))
        print("\n✅ Monitoring stopped")

if __name__ == "__main__":
    monitor_ml_model()
