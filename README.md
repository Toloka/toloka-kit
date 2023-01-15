# Toloka-Kit

[![License](https://img.shields.io/pypi/l/toloka-kit.svg)](https://github.com/toloka/toloka-kit/blob/master/LICENSE)
[![PyPI Latest Release](https://img.shields.io/pypi/v/toloka-kit.svg)](https://pypi.org/project/toloka-kit/)
[![Supported Versions](https://img.shields.io/pypi/pyversions/toloka-kit.svg)](https://pypi.org/project/toloka-kit)
[![Downloads](https://pepy.tech/badge/toloka-kit/month)](https://pepy.tech/project/toloka-kit)

[![Coverage](https://codecov.io/gh/Toloka/toloka-kit/branch/main/graph/badge.svg)](https://codecov.io/gh/Toloka/toloka-kit)
[![GitHub Tests](https://github.com/Toloka/toloka-kit/workflows/Tests/badge.svg?branch=main)](//github.com/Toloka/toloka-kit/actions?query=workflow:Tests)


[**<span style="color:red">Documentation</span>**](https://toloka.ai/en/docs/toloka-kit/?utm_source=github&utm_medium=site&utm_campaign=tolokakit)

[Website](https://toloka.ai/?utm_source=github&utm_medium=site&utm_campaign=tolokakit) |
[API Documentation](https://toloka.ai/en/docs/api/?utm_source=github&utm_medium=site&utm_campaign=tolokakit) |
[Platform](http://platform.toloka.ai/?utm_source=github&utm_medium=site&utm_campaign=tolokakit)


Designed by engineers for engineers, Toloka lets you integrate an on-demand workforce directly into your processes. Our cloud-based crowdsourcing platform is a fast and efficient way to collect and label large data sources for machine learning and other business purposes.

Main advantages of Toloka:
  - **Top-quality data** -  Collect and annotate training data that meets and exceeds industry quality standards thanks to multiple quality control methods and mechanisms available in Toloka.
  - **Scalable projects** - Have any amounts of image, text, speech, audio, or video data collected and labeled for you by millions of skilled Toloka users across the globe.
  - **Cost-efficiency** - Save time and money with this purpose-built platform for handling large-scale data collection and annotation projects, on-demand 24/7, at your own price and within your timeframe.
  - **Free, powerful API** - Build scalable and fully automated human-in-the-loop machine learning pipelines with a powerful open API.

**⚠️ toloka-kit==1.0.0 breaking changes ⚠️**

Starting with 1.0.0 release only the core version of the package is installed by default. See "Optional dependencies"
section for details.

Requirements
--------------
- Python 3.7+
- Register in [Toloka.ai](https://toloka.ai/?utm_source=github&utm_medium=site&utm_campaign=tolokakit) as requester. Registration process described [here](https://toloka.ai/en/docs/guide/concepts/access?utm_source=github&utm_medium=site&utm_campaign=tolokakit).
- [Topping up your account](https://toloka.ai/en/docs/guide/concepts/refill.html?utm_source=github&utm_medium=site&utm_campaign=tolokakit).
- Getting an OAuth. Learn more in [help](https://toloka.ai/en/docs/api/concepts/access?utm_source=github&utm_medium=site&utm_campaign=tolokakit) and in the image below.


![How to get OAuth token](https://yastatic.net/s3/doc-binary/src/support/toloka/en/toloka-kit/learn-basics/get-oauth-token.png "How to get OAuth token")

Get Started
--------------
Installing toloka-kit is as easy as:
```
$ pip install toloka-kit
```
Note: this project is still under heavy development and interfaces may change slightly. For production environments please specify exact package version. For example: `toloka-kit==0.1.26`

### Optional dependencies
If you want to install toloka-kit with all additional dependencies:
```shell
$ pip install toloka-kit[all]
```
or install only required extra dependencies (see our [documentation](https://toloka.ai/en/docs/toloka-kit/?utm_source=github&utm_medium=site&utm_campaign=tolokakit)):
```shell
$ pip install toloka-kit[pandas,autoquality,s3,zookeeper,jupyter-metrics]  # remove unnecessary requirements from the list
```

**Try your first program and checks the validity of the OAuth token:**
```python
import toloka.client as toloka

toloka_client = toloka.TolokaClient(input("Enter your token:"), 'PRODUCTION')
print(toloka_client.get_requester())
```

Useful Links
--------------
- [Toloka homepage](https://toloka.ai/?utm_source=github&utm_medium=site&utm_campaign=tolokakit).
- [Toloka requester's guide](https://toloka.ai/en/docs/?utm_source=github&utm_medium=site&utm_campaign=tolokakit).
- We recommend that you first get acquainted with Toloka through the web interface and implement [one of the tutorials](https://toloka.ai/en/docs/guide/concepts/usecases?utm_source=github&utm_medium=site&utm_campaign=tolokakit).
- [Toloka API documentation](https://toloka.ai/en/docs/api/?utm_source=github&utm_medium=site&utm_campaign=tolokakit).
- [Toloka-kit usage examples](https://github.com/Toloka/toloka-kit/tree/main/examples#toloka-kit-usage-examples).

Questions and bug reports
--------------
* For reporting bugs please use the [Toloka/bugreport](https://github.com/Toloka/toloka-kit/issues) page.
* Join our English-speaking [slack community](https://toloka.ai/community?utm_source=github&utm_medium=site&utm_campaign=tolokakit) for both tech and abstract questions.


Contributing
-------
Feel free to contribute to toloka-kit. Right now, we really need more [usage examples](https://github.com/Toloka/toloka-kit/tree/main/examples#need-more-examples).

License
-------
© YANDEX LLC, 2020-2021. Licensed under the Apache License, Version 2.0. See LICENSE file for more details.
