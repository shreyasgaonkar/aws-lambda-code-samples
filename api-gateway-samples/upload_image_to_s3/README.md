This function will upload a binary image file sent from a POST request from API Gateway with a proxy Lambda function integration. This will decode the binary string file, create an image file in the /tmp directory and call S3 to upload the object.

Replace `S3_BUCKET_NAME` to point to your S3 bucket assuming in the same region as that of the Lambda function. If not, override using `region_name=region_name` argument in the S3 client. To name the file, add `filename: MyFile.png` header in the POST request, otherwise create a random file with name: sample_file_{random}.png
