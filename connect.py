import requests

url = "http://54.165.184.178:5000/api/v1/states"
headers = {"Content-Type": "application/json"}
data = {
    "name": "New State"
}

response = requests.post(url, headers=headers, data=data)
print(response.status_code)
print(response.text)
