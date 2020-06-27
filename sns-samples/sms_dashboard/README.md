[sms_dashboard.py](sms_dashboard.py.py) will provide you additional insights on your SMS usage for a month pulling data from SMS Usage Reports stored in Amazon S3. Once enable, this script will pull a month's data (defaults to current month), extracts the **total parts**, **message types**, and the **mobile endpoint** where SMS were sent; and displays in a tablular dashboard using PrettyTable (can be added as a Lambda layer from [here](/lambda-layer/prettyTable.zip)).

By default, this will use the current aws region, month and year, but can be overiden to use specific month/year by changing:
```
# ==================
# REGION_NAME = 'us-east-1'
# YEAR = '2020'
# MONTH = '04'
# ==================
```

If you don't want to display any of the following dashboard, simply comment the lines:

```
print(f"SMS Dashboard for {MONTH}/{YEAR}")
print(DASH_TABLE)
print("\n")
print(COUNTRY_TABLE)
print("\n")
print(PHONE_NUMBER_TABLE)
```


### Output
```
SMS Dashboard for 06/2020
+---------------+--------+
|      Type     | Count  |
+---------------+--------+
| Transactional |  100   |
|   Total SMS   |  100   |
|  Total Price  | 0.645‬0 |
|  Total Parts  |  100   |
+---------------+--------+


+---------+--------------------+
| Country | Number of Messages |
+---------+--------------------+
|    US   |        100         |
+---------+--------------------+


+--------------+--------------------+
|   Endpoint   | Number of Messages |
+--------------+--------------------+
| +16692XXXXXX |         25         |
| +14698XXXXXX |         25         |
| +13473XXXXXX |         25         |
| +12018XXXXXX |         25         |
+--------------+--------------------+
```

### Prefer the CLI?
Refer to https://github.com/shreyasgaonkar/aws-cli-code-samples/tree/master/sns-samples/sms-dashboard for this minimal output:
```
Total SMS sent: 50
```
