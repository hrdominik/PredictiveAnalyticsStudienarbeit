import requests

query = {'headlines': ['Shares of several utility companies are trading']}


response = requests.post("http://127.0.0.1:8080/predict", json = query)
print(response.json())