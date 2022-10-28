import requests

response = requests.get(
    url="http://43.142.162.144:5000/addUser",
    params={"name": "test", "face_id": "test", "isAdmin": "false"},
)

print(response.text)
