import telnetlib


def lambda_handler(event, context):
    """ Main function """

    host = "www.google.com"
    port = "443"

    telnet_obj = telnetlib.Telnet(host, port)
    print(telnet_obj)  # Returns 200 status code for valid connection, else will timeout
