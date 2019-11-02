This will iterate through all functions in a region (defaults to where Lambda resides) to return the total size in MBs used by Lambda.

The default code storge limit per region is 75 GB as per the [documentation](https://docs.aws.amazon.com/lambda/latest/dg/limits.html):


```
+----------------------------+---------------+
|          Resource          | Default Limit |
+----------------------------+---------------+
| Concurrent executions      | 1,000         |
| Function and layer storage | 75 GB         |
+----------------------------+---------------+
```
