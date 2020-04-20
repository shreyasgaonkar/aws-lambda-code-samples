import telnetlib


HOST_NAME = "google.com"
PORT_NUMBER = "443"


def lambda_handler(event, context):
    """Main function"""

    try:
        telnet_obj = telnetlib.Telnet(HOST_NAME, PORT_NUMBER, timeout=3)
        status_code = 200
        response_message = f"Connection established at host {HOST_NAME} over port {PORT_NUMBER}. Closing connection."
        telnet_obj.close()

    except (ConnectionRefusedError, IOError):
        status_code = 504
        response_message = f"Cannot connect to {HOST_NAME} over port {PORT_NUMBER}. Please check the host name, port and/or network configurations."

    except Exception as unhandled_exception:
        status_code = 504
        response_message = f"Error: {unhandled_exception}. Cannot connect to {HOST_NAME} over port {PORT_NUMBER}."

    finally:
        return {
            "statusCode": status_code,
            "body": response_message
        }
