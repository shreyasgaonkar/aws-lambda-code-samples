[extract_deployment_package_without_layers.py](extract_deployment_package_without_layers.py) will attempt to separate out the Lambda function's deployment package from the layers.

Update the following variables before proceding:
```
LAMBDA_FUNCTION = 'my-function'
LAMBDA_REGION = 'us-east-1'
S3_BUCKET_NAME = 'my-bucket'
S3_OBJECT_NAME = 'lambda.zip'
```


While making any updates to the function's config when using Layers, Lambda will squash the deployment package (Lambda's code) along with all the layers into one file. This we can't extract the function code through any API calls, I've added this workaround with downloading the entire deployment package and the layers package and the difference between the files would be the function code added.

This will return a presigned URL from your S3 bucket to download the code.


Flow:
1. Get entire deployment package and extract it at /tmp/deployment_package using ```GetFunction``` API
2. Get all layers package and extract it at /tmp/layer_package using ```GetVersionLayer``` API
3. Compare for diff, any non hidden file(s)/directory will be used in #4
4. Create zip and upload it to S3
5. Create presigned url and return to client
