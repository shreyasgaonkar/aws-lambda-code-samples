[This script](lambda_code_size_including_layers.py) will return function size in MegaBytes inclusive of all attached layers. Currently, the deployment package size of the function including all of its layers should be [less than 250 MB unzipped](https://docs.aws.amazon.com/lambda/latest/dg/limits.html).

Sample output:
```
Total code size: 1012 bytes
Total layer size: 74264045 bytes
Total function size including layers: 72524.47 MB
```
