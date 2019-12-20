This will iterate through all functions in a region (defaults to where Lambda resides) to return the function name where ```Reserve concurrency``` is set - easier to find functions which might be using up the [Unreserved account concurrency](https://aws.amazon.com/about-aws/whats-new/2017/11/set-concurrency-limits-on-individual-aws-lambda-functions/).

[Newly introduced](https://aws.amazon.com/about-aws/whats-new/2019/12/aws-lambda-announces-provisioned-concurrency/) provisioned concurrency can also contribute towards reducing the Unreserved account concurrency count as seen on the dashboard. ```get_provisioned_concurrency_config()``` can be used to extract the reserved concurrency information off a version or alias.


**Note**:```client.get_provisioned_concurrency_config & client.get_function_concurrency()``` might require a newer boto3 version client. I have used boto3 v1.10.42, and you can check that using ```boto3.__version__```.


**Output**

```
Reserved concurrency:
my_function_1: 10
my_function_2: 5
=====================
Provisioned concurrency:
other_function: 50
```
