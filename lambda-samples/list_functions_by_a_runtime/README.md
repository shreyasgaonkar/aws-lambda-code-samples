## List Lambda functions by a runtime

[This function](list_functions_by_a_runtime.py) lists all Lambda functions (and versions) in a region mapping to a target runtime. This is helpful if you are trying to list all functions using a deprecated or near deprecation runtimes.

Provide the input parameters:

```python
...
REGION_NAME = 'us-west-2'
...

```

Output:

```
+------------------------------------------------------------------------+-----------------+-----------+
|                              Function Arn                              |  Function Name  |  Runtime  |
+------------------------------------------------------------------------+-----------------+-----------+
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:default_logging:$LATEST | default_logging | python2.7 |
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:boto3_python27:$LATEST  |  boto3_python27 | python2.7 |
|   arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:tmp_content:$LATEST   |   tmp_content   | python2.7 |
|   arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:insights_2:$LATEST    |    insights_2   | python2.7 |
|   arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:cw_insights:$LATEST   |   cw_insights   | python2.7 |
|    arn:aws:lambda:us-west-2:XXXXXXXXXXXX:function:python27:$LATEST     |     python27    | python2.7 |
+------------------------------------------------------------------------+-----------------+-----------+
Total Lambda function versions using python2.7 Runtime: 6
```
