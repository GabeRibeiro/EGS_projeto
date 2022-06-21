# pip install requests
import requests 
import datetime

print("_________________ PRINT __________________")
r = requests.get('http://localhost:41181/URL/Print',headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()
# 193.136.173.103
print("_________________ ADD PARKING BASIC URL REQUEST __________________")
r = requests.put('http://localhost:41181/URL/Add/Basic',{"user_id": 1,"url":"http://services.web.ua.pt/parques/parques","value":"Livre","tag":"Nome"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

r = requests.put('http://localhost:41181/URL/Add/Basic',{"user_id": 1,"url":"http://193.136.173.103/parques/parques","value":"Livre","tag":"Nome"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://localhost:41181/URL/Print',{"user_id": 1},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
"""
r = requests.put('http://localhost:41181/URL/Add/Token',{"user_id": 1,"url":'http://193.136.173.103/parques/parques',"value":"Livre","tag":"Nome","token_url":'http://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

r = requests.put('http://localhost:41181/URL/Add/Token',{"user_id": 1,"url":'http://193.136.173.103/parques/parques',"value":"Livre","tag":"Nome","token_url":'http://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD KEY PARKING URL REQUEST __________________")
r = requests.put('http://localhost:41181/URL/Add/Key',{"user_id": 1,"url":"http://193.136.173.103/parques/parques","key":"dummy","value":"Livre","tag":"Nome"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD HTTP PARKING URL REQUEST __________________")
r = requests.put('http://localhost:41181/URL/Add/Http',{"user_id": 1,"url":"http://193.136.173.103/parques/parques","key":"dummy","username":"dummy","value":"Livre","tag":"Nome"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
"""
print("_________________ PRINT __________________")
r = requests.get('http://localhost:41181/URL/Print',headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()

print("_________________ Pause __________________")
r = requests.post('http://localhost:41181/URL/Pause',{"user_id":1,"metric_id":1},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://localhost:41181/URL/Print',headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()

print("_________________ Remove __________________")
r = requests.post('http://localhost:41181/URL/Remove',{"user_id":1,"metric_id":6},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:41181/URL/Remove',{"user_id":1,"metric_id":7},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:41181/URL/Remove',{"user_id":1,"metric_id":8},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:41181/URL/Remove',{"user_id":1,"metric_id":9},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:41181/URL/Remove',{"user_id":1,"metric_id":11},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://localhost:41181/URL/Print',headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()


print("_________________ FILTER INTERVAL _________________")
r = requests.get('http://localhost:41181/URL/Filter/Interval',{"metric_id":13,"user_id":1,"upper_limit":"2022-08-20 23:00:00","lower_limit":"2022-06-20 00:00:00","tag":"ZTC"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()

r = requests.get('http://localhost:41181/URL/All',{"user_id":1},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})

r = requests.get('http://localhost:41181/URL/Cheat',{"sql":"SELECT * FROM Value"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})

r = requests.get('http://localhost:41181/URL/Cheat',{"sql":"SELECT Value.timestamp,Value.tag,Value.value FROM Value,Basic_url WHERE Basic_url.metric_id=22 AND Basic_url.user_id=1 AND Value.tag='ZTC' AND timestamp >= '2022-06-20 00:00:00' AND timestamp <= '2022-08-20 00:00:00'"},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})

r = requests.get('http://localhost:41181/URL/Cheat',{"sql":'SELECT MAX(metric_id) FROM Basic_url'},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})

r = requests.get('http://localhost:41181/URL/Cheat',{"sql":'SELECT * FROM Basic_url WHERE metric_id = %s'},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})

r = requests.post('http://localhost:41181/URL/Start',{"metric_id":8, "user_id":1},headers={'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})

#r = requests.get('http://localhost:46833/verifyToken',headers={"auth-token":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIxZTgxNzI0MDZhZGRkYTcyNzYyOWQiLCJpYXQiOjE2NTU4MjY0NzAsImV4cCI6MTY1NTg0ODA3MH0.mi_FMqetMsEZ9Dbvz4PTnZOkHWrVT_T7mkduMYNnGP8'})