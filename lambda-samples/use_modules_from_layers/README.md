```use_modules_from_layers.py``` help in bumping up the priority of the modules imported off Lambda layers when your deployment package also contains another version. While modules/libraries from layers are automatically added to the PYTHONPATH, with using both deployment package module and layer, Lambda picks up the module from the deployment package (/var/task) aka the root directory where Lambda function is loaded from. We can override this using the `sys.path.insert()` python method. Use the import statements after updating sys path for this to work.

As an sample here, I've used Python's [urllib3](https://pypi.org/project/urllib3/) module and added as a Python layer to a sample Lambda function. If you need help creating a Python Layer, I've written a blog post here: https://medium.com/@shreyasgaonkar/managing-python-modules-in-aws-lambda-layers-c9482b646e69 or use the sample layer from [here](lambda-layer/urllib3.zip).


### Output:

```
urllib3 imported from: /opt/python/urllib3/__init__.py
urllib3 version loaded: 1.26.6
```
