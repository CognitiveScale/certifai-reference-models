import requests
import json
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(f'{dir_path}/../test_instances.json', 'rb') as f:
    test_msg = json.load(f)

for model in ['dtree', 'logit', 'mlp', 'svm']:
    r = requests.post(f'http://127.0.0.1:5111/german_credit_{model}/predict', json=test_msg)
    print(f'Response from dtree/predict: [{r.status_code}] {r.text}')
    assert(r.status_code == 200)

r = requests.get('http://127.0.0.1:5111/health', json=test_msg)
print(f'Response from health: [{r.status_code}] {r.text}')
assert(r.status_code == 200)

r = requests.post('http://127.0.0.1:5111/shutdown', json=test_msg)
print(f'Response from shutdown: [{r.status_code}] {r.text}')
assert(r.status_code == 200)

