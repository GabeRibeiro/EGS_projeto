# pip install requests
import requests 

print("_________________ PRINT __________________")
r = requests.get('http://localhost:40109/URL/Print',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()

print("_________________ ADD PARKING BASIC URL REQUEST __________________")
r = requests.put('http://localhost:40109/URL/Add/Basic',{"user_id": 1,"url":"http://services.web.ua.pt/parques/parques","value":"Livre","tag":"Nome"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://localhost:40109/URL/Print',{"user_id": 1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
"""
r = requests.put('http://localhost:40109/URL/Add/Token',{"user_id": 1,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"value":"Livre","tag":"Nome","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

r = requests.put('http://localhost:40109/URL/Add/Token',{"user_id": 1,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"value":"Livre","tag":"Nome","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD KEY PARKING URL REQUEST __________________")
r = requests.put('http://localhost:40109/URL/Add/Key',{"user_id": 1,"url":"http://services.web.ua.pt/parques/parques","key":"dummy","value":"Livre","tag":"Nome"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD HTTP PARKING URL REQUEST __________________")
r = requests.put('http://localhost:40109/URL/Add/Http',{"user_id": 1,"url":"http://services.web.ua.pt/parques/parques","key":"dummy","username":"dummy","value":"Livre","tag":"Nome"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
"""
print("_________________ PRINT __________________")
r = requests.get('http://localhost:40109/URL/Print',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()

print("_________________ Pause __________________")
r = requests.post('http://localhost:40109/URL/Pause',{"user_id":1,"id":1},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://localhost:40109/URL/Print',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()

print("_________________ Remove __________________")
r = requests.post('http://localhost:40109/URL/Remove',{"user_id":1,"id":6},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:40109/URL/Remove',{"user_id":1,"id":7},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:40109/URL/Remove',{"user_id":1,"id":8},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:40109/URL/Remove',{"user_id":1,"id":9},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()
r = requests.post('http://localhost:40109/URL/Remove',{"user_id":1,"id":10},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://localhost:40109/URL/Print',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
if r.status_code < 400:
    print(r)
for entry in r.json():
    print(entry)
print()
