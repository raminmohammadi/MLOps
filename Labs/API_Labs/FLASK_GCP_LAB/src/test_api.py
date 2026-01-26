import requests
import json

url = 'http://127.0.0.1:8080/predict'

payload = {
    'sepal_length': 5.1,
    'sepal_width': 3.5,
    'petal_length': 1.4,
    'petal_width': 0.2
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print("Status:", response.status_code)
print("Body:", response.text)

if response.status_code == 200:
    try:
        prediction = response.json()['prediction']
        print('Predicted species:', prediction)
    except Exception as e:
        print("Could not parse JSON:", e)
else:
    print('Error:', response.status_code)