# Copyleaks Python SDK
Copyleaks (http://www.copyleaks.com) Python SDK

### Installing dependencies

Create a virtual environment and install dependencies from requirements.txt by running (from the root):

```
> pip install -r requirements.txt
```
### Setup

You can setup the project by downloading the source code and then running the following command:

```
> python setup.py install
```

Once installed you should get your API key from http://copyleaks.com and you can get started. For example, here
is how you can count credits

```
>>> from copyleaks_sdk.copyleaks import CopyLeaks
>>> self.copyleak = CopyLeaks(YOUR USERNAME HERE, API KEY HERE)
>>>
>>> def test_count_credits(self):
>>>     credit = self.copyleak.count_credits()
```

And here is how you can create a process by file:

```
>>> response = self.copyleak.create_process_by_file('full_path_of_file.txt')
```

### License

This project is licensed under the terms of MIT license.

### Tests

You can find tests under copyleaks-python-sdk/tests. Tests are written the built-in unittest module and can simply
be run from the command line.
