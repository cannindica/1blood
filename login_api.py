import requests, json


# api_url_base = 'https://api.unira.ac.id/v1/'
# api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE1NDY2NzQ3NjQsImp0aSI6NDA4MiwiZXhwIjoxNTQ2Njc1MzY0LCJpc3MiOiJ1bmlyYS5hYy5pZCIsImRhdCI6eyJpZCI6Im00MDgyaDIwMTM1MjUwMDJzIiwicHJvZGkiOjUyLCJ0eXBlIjoibWhzIiwiYWNjZXNzIjpudWxsfX0.LINeYgj5MT7EGjjdsK1dch33KbwwxHHcegLgTwhn3C2TI-IVIohlj5roNNjVY4QLkNhZ5uKVted8j9KCX7NbkA'

# headers = {
# 	'Content-Type': 'application/json',
# 	'Authorization': 'Bearer {0}'.format(api_token)
# }

# api_saya = '{0}saya'.format(api_url_base)

# response = requests.get(api_saya, headers=headers)

# if response.status_code == 200:
# 	detail_saya = json.loads(response.content.decode('utf-8'))
# else:
# 	detail_saya = "Authentication Error"

# print(response.status_code)

# print(detail_saya)

username = input("Username : ")
password = input("Password : ")

data = {
	'username': username,
	'password': password,
}

validation_api = requests.post(url="https://api.unira.ac.id/v1/token", data=data)

if validation_api.status_code != 201:
	print("Login API 1st failed !!!")
else:
	dva = json.loads(validation_api.content.decode('utf-8'))
	token_api = str(dva["data"]["attributes"]["access"])
	print(validation_api.status_code)
	print(token_api)
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer {0}'.format(token_api),
	}
	print(headers)
	api_saya = requests.get("https://api.unira.ac.id/v1/saya", headers=headers)
	if api_saya.status_code != 200:
		print("Login API 2nd failed !!!")
		print(api_saya)
	else:
		detail_saya = json.loads(api_saya.content.decode('utf-8'))
		print(detail_saya["data"]["attributes"]["prodi"])
		print(detail_saya["data"]["id"])


	print(api_saya.status_code)
# print(username, password)