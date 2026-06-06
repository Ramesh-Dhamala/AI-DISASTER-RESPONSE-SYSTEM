#!/bin/bash

BASE_URL="http://localhost:5000"

echo "====================================="
echo "Testing All API Endpoints"
echo "====================================="

# 1. Health Check
echo -e "\n1. Health Check:"
curl -s ${BASE_URL}/health | python -m json.tool

# 2. Model Info (NEW)
echo -e "\n2. Model Info:"
curl -s ${BASE_URL}/model-info | python -m json.tool

# 3. List Models (NEW)
echo -e "\n3. List Available Models:"
curl -s ${BASE_URL}/api/models | python -m json.tool

# 4. Text Prediction
echo -e "\n4. Text Classification:"
curl -s -X POST ${BASE_URL}/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "earthquake building collapse"}' | python -m json.tool

# 5. Landslide Prediction
echo -e "\n5. Landslide Risk Prediction:"
curl -s -X POST ${BASE_URL}/api/predict/landslide \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240}' | python -m json.tool

# 6. Flood Prediction
echo -e "\n6. Flood Risk Prediction:"
curl -s -X POST ${BASE_URL}/api/predict/flood \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240}' | python -m json.tool

# 7. Earthquake Prediction
echo -e "\n7. Earthquake Risk Prediction:"
curl -s -X POST ${BASE_URL}/api/predict/earthquake \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240}' | python -m json.tool

# 8. All Disasters Prediction
echo -e "\n8. All Disasters Prediction:"
curl -s -X POST ${BASE_URL}/api/predict/all \
  -H "Content-Type: application/json" \
  -d '{"latitude": 27.7172, "longitude": 85.3240}' | python -m json.tool

echo -e "\n====================================="
echo "Testing Complete"
echo "====================================="
