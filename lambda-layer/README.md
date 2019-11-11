You can use these ```.zip``` files in your projects by creating a layer and adding it to the required layers. Make sure to select the required runtimes for these layers for your functions to list them under the console.

```
boto3.zip -> boto3 version 1.10.2

requests.zip -> Useful if you were relying on the vendored version of request module off the botocore now that has been stripped off the SDK.

pandasnumpy.zip -> includes pandas numpy scipy modules. You might have to upload it to S3 and reference the URL under the Lambda's layer console.

psycopg2.zip -> runs on python2.7 following [jkehler](https://github.com/jkehler/awslambda-psycopg2) repo
```
