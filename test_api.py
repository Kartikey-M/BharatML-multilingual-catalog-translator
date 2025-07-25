import requests
import json

# Test the API directly
url = "http://localhost:8000/translate"
data = {
    "text": "Broom",
    "source_language": "en", 
    "target_language": "hi"
}

try:
    response = requests.post(url, json=data)
    result = response.json()
    print("API Response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
