## Python3.8+
For Python3.8+ runtimes, use the modules from `python3.8+` directory. For other earlier runtimes, use the .zip from this directory.


You can use these ```.zip``` files in your projects by creating a layer and adding it to the required layers. Make sure to select the required runtimes for these layers for your functions to list them under the console.

Unlike deployment packages, modules for layers have to be bundled inside a [directory](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path). For python that directory is 'python'. The folder structure would look something like this:

```
pillow.zip
│ python/PIL
└ python/Pillow-5.3.0.dist-info
```

boto3.zip -> boto3 version 1.10.2

requests.zip -> Useful if you were relying on the vendored version of request module off the botocore now that has been [stripped off the SDK](https://aws.amazon.com/blogs/developer/removing-the-vendored-version-of-requests-from-botocore/).

pandasnumpy.zip -> includes pandas numpy scipy modules. You might have to upload it to S3 and reference the URL under the Lambda's layer console.

psycopg2.zip -> runs on python2.7 following [jkehler](https://github.com/jkehler/awslambda-psycopg2) repo
