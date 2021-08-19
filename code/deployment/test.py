import requests

data = {'headlines': ['Shares of several utility companies are trading', 'stock very high best apple low']}

response = requests.post("http://127.0.0.1:80/predict", json = data)

print(response.json())