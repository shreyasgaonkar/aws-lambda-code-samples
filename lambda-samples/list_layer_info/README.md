```list_layer_info.py``` will iterate through all layers and it's versions to return information about the layer. Function uses [Paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#paginators) to iterate through all layers, and it's versions.

Uses [PrettyTable](https://pypi.org/project/PrettyTable/) module imported as a Lambda layer from [here](/lambda-layer/).

### Output:

```
+-------------------------------------------------------+-----------+-----------------+-------------------------------------------------------+
|                       LayerARN                        |  Version  |  CodeSize (MB)  |                  Compatible Runtimes                  |
+-------------------------------------------------------+-----------+-----------------+-------------------------------------------------------+
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:layer:Jython    |        1  |           0.03  |  ['java8', 'python2.7', 'python3.6', 'python3.7']     |
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:layer:X-Ray     |        2  |           9.09  |  ['python2.7', 'python3.6', 'python3.7', 'python3.8'] |
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:layer:X-Ray     |        1  |           9.14  |  ['python2.7', 'python3.6', 'python3.7', 'python3.8'] |
| arn:aws:lambda:us-west-2:XXXXXXXXXXXX:layer:requests  |        1  |           0.95  |  ['python2.7', 'python3.6', 'python3.7']              |
+-------------------------------------------------------+-----------+-----------------+-------------------------------------------------------+
```

#### Additional Context:

Response of ```list_layer_versions()```:

```JSON
{
    "LayerVersionArn": "arn:aws:lambda:us-west-2:XXXXXXXXXXXX:layer:my_lambda_layer:5",
    "Version": 5,
    "Description": "Layer description,
    Numpy&SciPy",
    "CreatedDate": "2019-10-25T18:57:17.095+0000",
    "CompatibleRuntimes": [
        "python2.7",
        "python3.6",
        "python3.7"
    ]
}
```

We can make a second call using the ```LayerVersionArn``` parameter of the above call into ```get_layer_version()``` call.

```list_layer_versions()``` returns the LayerVersionArn having the version number in it. To call the ```get_layer_version()``` API, we would need to clean it using regex:

```python
layer_arn = re.split(r':', i['LayerVersionArn'])
layer_arn = ":".join(layer_arn[:-1])
```
