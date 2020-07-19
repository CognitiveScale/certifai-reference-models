import requests
import json

with open(f'test_instances.json', 'rb') as f:
    test_msg = json.load(f)

r = requests.post('http://127.0.0.1:8551/predict', json=test_msg)
print(f'Response from model: [{r.status_code}] {r.text}')

r = requests.get('http://127.0.0.1:8551/health', json=test_msg)
print(f'Response from health: [{r.status_code}] {r.text}')

r = requests.post('http://127.0.0.1:8551/shutdown', json=test_msg)
print(f'Response from shutdown: [{r.status_code}] {r.text}')
