import urllib.request
import json

def lambda_handler(event, context):
    a=urllib.request.urlopen('http://www.google.com/')
    print(a.getcode()) # Returns 200 status code for valid connection, else will timeout
