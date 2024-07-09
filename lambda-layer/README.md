# Lambda python layers

For Python3.8+ runtimes, use the modules from `python3.8+` directory. For other earlier runtimes, use the .zip from this root directory.

## Versions

```bash
python38+
│ boto3_python38+.zip (v1.18.42)
│ numpy_pandas_scipy_python38+.zip
    │ scipy (v1.4.1)
    │ numpy (v1.20.3)
    └ pandas (v1.3.3)
│ urllib3.zip (v1.26.6)
└ requests_python38+.zip (v2.26.0)
```

```bash
.
│ boto3.zip (v1.10.2)
│ pandasnumpy.zip
    │ scipy (v1.3.1)
    │ numpy (v1.17.3)
    └ pandas (v0.25.2)
│ psycopg2.zip
│ requests.zip (v2.22.0)
│ urllib3.zip (v1.26.6)
│ x-ray.zip
└ prettyTable.zip
```

You can use these `.zip` files in your projects by creating a layer and adding it to the required layers. Make sure to select the required runtimes for these layers for your functions to list them under the console.

---

Unlike deployment packages, modules for layers have to be bundled inside a [directory](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path). For python that directory is 'python'. The folder structure would look something like this:

```bash
pillow.zip
│ python/PIL
└ python/Pillow-5.3.0.dist-info
```

## Additional Info

1. `requests.zip` -> Useful if you were relying on the vendored version of request module off the botocore now that has been [stripped off the SDK](https://aws.amazon.com/blogs/developer/removing-the-vendored-version-of-requests-from-botocore/).

2. `pandasnumpy.zip` -> includes pandas numpy scipy modules. You might have to upload it to S3 and reference the URL under the Lambda's layer console if the .zip is larger than 50MBs.

3. `psycopg2.zip` -> runs on python2.7 following [jkehler](https://github.com/jkehler/awslambda-psycopg2) repo
