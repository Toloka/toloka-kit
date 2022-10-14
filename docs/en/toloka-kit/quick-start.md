# Quick Start

To start with Toloka-Kit:

1. Get an OAuth token in your [profile](https://toloka.yandex.com/requester/profile/integration) or in the [Sandbox profile](https://sandbox.toloka.yandex.com/requester/profile/integration).

2. Install the Toloka-Kit package:

    ```shell
   $ pip install toloka-kit[all]
   ```
   or install only required dependencies:
   ```shell
   $ pip install toloka-kit[pandas,autoquality,s3,zookeeper,jupyter-metrics]
   # or just the core version
   $ pip install toloka-kit
    ```

3. Check access to the API with the following Python script. The script:
    * Imports the package.
    * Asks to enter the OAuth token.
    * Requests general information about your account.

    ```python
    import toloka.client as toloka

    target = 'SANDBOX'      # Send requests to the Sandbox
    # target = 'PRODUCTION' # Uncomment to send requests to the production version

    toloka_client = toloka.TolokaClient(input("Enter your token:"), target)
    print(toloka_client.get_requester())
    ```

## What's Next

* Complete one of the [tutorials](https://toloka.ai/docs/guide/concepts/usecases.html) to get acquainted with Toloka web interface.
* Try [Toloka-Kit usage examples](https://github.com/Toloka/toloka-kit/tree/main/examples#toloka-kit-usage-examples).
* Read the package reference starting with [TolokaClient](https://toloka.ai/docs/toloka-kit/reference/toloka.client.TolokaClient.html).
* Study [Toloka API documentation](https://toloka.ai/docs/api/concepts/about.html/).
* See other features in [Toloka requester's guide](https://toloka.ai/docs/guide/index.html).
* Contribute to [Toloka-Kit on GitHub](https://github.com/Toloka/toloka-kit): open pull requests, report bugs or share your [usage examples](https://github.com/Toloka/toloka-kit/tree/main/examples#need-more-examples).
