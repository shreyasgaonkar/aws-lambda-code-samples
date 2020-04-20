Often times we need to check if Lambda has internet - super useful if the function is inside VPC.

#### Outputs:

Successful request:

``` {'statusCode': 200, 'body': 'Connection established at host google.com over port 443. Closing connection.'} ```

Unable to connect to the endpoint:

``` {'statusCode': 504, 'body': 'Cannot connect to google.com over port 20000. Please check the host name, port and/or network configurations.'} ```
