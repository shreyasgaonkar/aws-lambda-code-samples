## ENIs created by Lambda

[This function](lambda_created_enis.py) lists all the ENIs created by all Lambda functions in a region.

Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module imported as a [Lambda layer](/lambda-layer/prettyTable.zip).


Output:
```

+-----------------------+--------+--------------+-----------------+-----------------------------------------------+
|         ENI ID        | Status |    VPC ID    |    Subnet Id    |                Security Groups                |
+-----------------------+--------+--------------+-----------------+-----------------------------------------------+
| eni-XXXXXXXXXXXXXXXXX | in-use | vpc-XXXXXXXX | subnet-XXXXXXXX |                ['sg-XXXXXXXX']                |
| eni-XXXXXXXXXXXXXXXXX | in-use | vpc-XXXXXXXX | subnet-XXXXXXXX |         ['sg-XXXXXXXX', 'sg-XXXXXXXX']        |
| eni-XXXXXXXXXXXXXXXXX | in-use | vpc-XXXXXXXX | subnet-XXXXXXXX | ['sg-XXXXXXXX', 'sg-XXXXXXXX', 'sg-XXXXXXXX'] |
+-----------------------+--------+--------------+-----------------+-----------------------------------------------+

```

Looking for an reverse use-case? Try [lambda_hyperplane_eni_checker](../lambda_hyperplane_eni_checker/)
