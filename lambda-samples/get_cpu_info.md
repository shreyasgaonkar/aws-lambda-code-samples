Simple script to get additional information about the underlying Lambda's hardware, /tmp storage, os-release and it's contents in python.

```
Lambda's default working directory:
/var/task
/tmp contents: []


Size of filesystem in MegaBytes: 525.8046875
Actual number of free MegaBytes: 524.953125
Number of free Megaytes: 513.39453125


cat /etc/os-release:
b'NAME="Amazon Linux AMI"\nVERSION="2018.03"\nID="amzn"\nID_LIKE="rhel fedora"\nVERSION_ID="2018.03"\nPRETTY_NAME="Amazon Linux AMI 2018.03"\nANSI_COLOR="0;33"\nCPE_NAME="cpe:/o:amazon:linux:2018.03:ga"\nHOME_URL="http://aws.amazon.com/amazon-linux-ami/"\nVARIANT_ID="201910291417-al2018.03.205.0"\n'


uname -a:
b'Linux 169.254.224.237 4.14.133-97.112.amzn2.x86_64 #1 SMP Wed Aug 7 22:41:25 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux\n'
````
