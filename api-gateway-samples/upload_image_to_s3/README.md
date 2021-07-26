[This function](https://github.com/shreyasgaonkar/aws-lambda-code-samples/blob/master/api-gateway-samples/upload_image_to_s3/upload_image_to_s3.py) will upload a binary image file sent from a POST request from API Gateway with a proxy Lambda function integration. It will decode the binary string file, create an image file in the /tmp directory and call S3 to upload the object.

Replace `S3_BUCKET_NAME` to point to your S3 bucket assuming in the same region as that of the Lambda function. If not, override using `region_name=region_name` argument in the S3 client. To name the file, add `filename: MyFile.png` header in the POST request, otherwise create a random file with name: sample_file_{random}.png

---

Replace the uri from `template.yml` to include the `AccountId` and the region of API Gateway and the [Lambda function](https://github.com/shreyasgaonkar/aws-lambda-code-samples/blob/master/api-gateway-samples/upload_image_to_s3/upload_image_to_s3.py).

```
arn:aws:apigateway:<api-region>:lambda:path/2015-03-31/functions/arn:aws:lambda:<lambda-region>:<Account-Id>:function:<Lambda-function-name>/invocations
```
