# tests/test_integration.py
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.services.integration import get_integration_service

def test_landslide_prediction():
    """Test landslide prediction endpoint"""
    service = get_integration_service()
    result = service.predict_landslide(40.7128, -74.0060)
    
    assert result['status'] == 'success'
    assert 'prediction' in result
    assert 'risk_score' in result['prediction']
    print(f"✅ Landslide test passed: Risk = {result['prediction']['risk_level']}")

def test_all_hazards():
    """Test all hazards prediction"""
    service = get_integration_service()
    result = service.predict_all_hazards(40.7128, -74.0060)
    
    assert result['status'] == 'success'
    assert 'overall_risk' in result
    print(f"✅ All hazards test passed: Overall risk = {result['overall_risk']['level']}")

if __name__ == '__main__':
    test_landslide_prediction()
    test_all_hazards()
    print("\n🎉 All tests passed!")