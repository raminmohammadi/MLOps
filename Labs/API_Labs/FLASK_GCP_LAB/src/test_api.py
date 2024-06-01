import requests

url = 'http://127.0.0.1:5000/predict'

data = {
    'sepal_length': 5.1,
    'sepal_width': 3.5,
    'petal_length': 1.4,
    'petal_width': 0.2
}

response = requests.post(url, data=data)

if response.status_code == 200:
    prediction = response.json()['prediction']
    print('Predicted species:', prediction)
else:
    print('Error:', response.status_code)