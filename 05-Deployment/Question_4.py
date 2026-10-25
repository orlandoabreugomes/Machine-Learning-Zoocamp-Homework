import requests

from fastapi import FastAPI
from pydantic import BaseModel

# health:

url = 'http://localhost:9696/health'
response = requests.get(url)
data = response.json()

print(f'response code: {response.status_code}')
print(f'status: {data["status"]}')

# predict:

lead = {
  "lead_source": "organic_search",
  "industry": "technology",
  "employment_status": "employed",
  "location": "europe",
  "number_of_courses_viewed": 4,
  "annual_income": 80304.0,
  "interaction_count": 7,
  "lead_score": 0.74
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=lead)
data = response.json()

print()
print(f'response code: {response.status_code}')
print(f'conversion probability: {data["conversion_probability"]:.3f}')
print(f'convertion: {data["conversion"]}')
