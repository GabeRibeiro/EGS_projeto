import requests 

print("_________________ PRINT __________________")
r = requests.get('http://127.0.0.1:5000/URL/Print',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

r = requests.put('http://127.0.0.1:5000/URL/Add/Token',{"id":11,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"args":"clientCount_2_4GHz, upTime, location, macAddress","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

r = requests.put('http://127.0.0.1:5000/URL/Add/Token',{"id":15,"url":'https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult=',"args":"clientCount_2_4GHz, upTime, location, macAddress","token_url":'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid',"secret":'BrszH8oF9QsHRjiOAC1D9Ze0Iloa',"auth_type":'Bearer',"content_type":'application/x-www-form-urlencoded',"key":'j_mGndxK2WLKEUKbGrkX7n1uxAEa','period':5},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD KEY PARKING URL REQUEST __________________")
r = requests.put('http://127.0.0.1:5000/URL/Add/Key',{"id":5,"url":"http://services.web.ua.pt/parques/parques","key":"dummy","args":"clientCount, location, macAddress"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD HTTP PARKING URL REQUEST __________________")
r = requests.put('http://127.0.0.1:5000/URL/Add/Http',{"id":6,"url":"http://services.web.ua.pt/parques/parques","key":"dummy","username":"dummy","args":"clientCount, location, macAddress"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ ADD PARKING BASIC URL REQUEST __________________")
r = requests.put('http://127.0.0.1:5000/URL/Add/Basic',{"id":8,"url":"http://services.web.ua.pt/parques/parques","args":"Nome, Ocupado,Capacidade,Livre"},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ PRINT __________________")
r = requests.get('http://127.0.0.1:5000/URL/Print',headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()

print("_________________ Remove __________________")
r = requests.post('http://127.0.0.1:5000/URL/Remove',{"id":11},headers={'Authorization':'ASDzxcdwekjkads786zxc123asdzxc98788ASd9231sz76238'})
print(r.status_code)
print(r.text)
if r.status_code < 400:
    print(r)
print()