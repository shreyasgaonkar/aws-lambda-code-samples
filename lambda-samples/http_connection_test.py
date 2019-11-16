import urllib.request


def lambda_handler(event, context):
    a = urllib.request.urlopen('http://www.google.com/')
    # Returns 200 status code for valid connection, else will timeout
    return a.getcode()
