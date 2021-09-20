# Toloka-Kit

[![License](https://img.shields.io/pypi/l/toloka-kit.svg)](https://github.com/toloka/toloka-kit/blob/master/LICENSE)
[![PyPI Latest Release](https://img.shields.io/pypi/v/toloka-kit.svg)](https://pypi.org/project/toloka-kit/)
[![Supported Versions](https://img.shields.io/pypi/pyversions/toloka-kit.svg)](https://pypi.org/project/toloka-kit)
[![Downloads](https://pepy.tech/badge/toloka-kit/month)](https://pepy.tech/project/toloka-kit)

[![Coverage](https://codecov.io/gh/Toloka/toloka-kit/branch/main/graph/badge.svg)](https://codecov.io/gh/Toloka/toloka-kit)
[![GitHub Tests](https://github.com/Toloka/toloka-kit/workflows/Tests/badge.svg?branch=main)](//github.com/Toloka/toloka-kit/actions?query=workflow:Tests)


[**<span style="color:red">Documentation</span>**](https://yandex.com/dev/toloka/toloka-kit/doc/)

[Website](https://toloka.ai) |
[API Documentation](https://yandex.ru/dev/toloka/doc/concepts/about.html?lang=en) |
[Platform](http://toloka.yandex.com)


Designed by engineers for engineers, Toloka lets you integrate an on-demand workforce directly into your processes. Our cloud-based crowdsourcing platform is a fast and efficient way to collect and label large data sources for machine learning and other business purposes.

Main advantages of Toloka:
  - **Top-quality data** -  Collect and annotate training data that meets and exceeds industry quality standards thanks to multiple quality control methods and mechanisms available in Toloka.
  - **Scalable projects** - Have any amounts of image, text, speech, audio, or video data collected and labeled for you by millions of skilled Toloka users across the globe.
  - **Cost-efficiency** - Save time and money with this purpose-built platform for handling large-scale data collection and annotation projects, on-demand 24/7, at your own price and within your timeframe.
  - **Free, powerful API** - Build scalable and fully automated human-in-the-loop machine learning pipelines with a powerful open API.


Requirements
--------------
- Python 3.6+
- Register in [Toloka.ai](https://toloka.ai/) as requester. Registration process described [here.](https://yandex.ru/support/toloka-requester/concepts/access.html?lang=en)
- [Topping up your account.](https://yandex.ru/support/toloka-requester/concepts/refill.html?lang=en)
- Getting an OAuth. Learn more in [help](https://yandex.ru/dev/toloka/doc/concepts/access.html?lang=en) and in the image below.


![How to get OAuth token](https://tlk.s3.yandex.net/toloka-kit/OAuth.png "How to get OAuth token")

Get Started
--------------
Installing toloka-kit is as easy as:
```
$ pip install toloka-kit
```
Note: this project is still under heavy development and interfaces may change slightly. For production environments please specify exact package version. For example: `toloka-kit==0.1.8`

**Try your first program and checks the validity of the OAuth token:**
```python
import toloka.client as toloka

toloka_client = toloka.TolokaClient(input("Enter your token:"), 'PRODUCTION')
print(toloka_client.get_requester())
```

Free trial
--------------
To get acquainted with Toloka tools for free, you can use the promo code **TOLOKAKIT1** on $20 on your [profile page](https://toloka.yandex.com/requester/profile) after registration.


Useful Links
--------------
- [Toloka homepage.](https://toloka.ai/)
- [Toloka requester's guide.](https://yandex.ru/support/toloka-requester/index.html?lang=en)
- We recommend that you first get acquainted with Toloka through the web interface and implement [one of the tutorials.](https://yandex.ru/support/toloka-requester/concepts/usecases.html)
- [Toloka API documentation.](https://yandex.com/dev/toloka/doc/concepts/about.html?lang=en)
- [Toloka-kit usage examples.](https://github.com/Toloka/toloka-kit/tree/main/examples#toloka-kit-usage-examples)

Questions and bug reports
--------------
* For reporting bugs please use the [Toloka/bugreport](https://github.com/Toloka/toloka-kit/issues) page.
* Join our English-speaking [slack community](https://toloka.ai/community) for both tech and abstract questions.


Contributing
-------
Feel free to contribute to toloka-kit. Right now, we really need more [usage examples.](https://github.com/Toloka/toloka-kit/tree/main/examples#need-more-examples)

License
-------
© YANDEX LLC, 2020-2021. Licensed under the Apache License, Version 2.0. See LICENSE file for more details.
