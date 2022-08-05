import requests
 
def login(password): # password is a string
    host = 'http://192.168.7.2:8181/api/login'
    a = requests.post(host, json={'username': 'admin', 'password': password}, verify=False)
    cookiejar = a.cookies
    return cookiejar

def set_spectrum_a(array,cookiejar): #  array is a list of integers
    host = 'http://192.168.7.2:8181/api/luminaire/1/command/SET_SPECTRUM_A'
    data = {'arg': array}
    requests.post(host,json=data,cookies = cookiejar,verify = False)

led_pass = '1b66c3cd5e475454'
cj = login(led_pass)

spect = [0, 0, 0, 0, 0, 0, 0]
set_spectrum_a(spect, cj)    