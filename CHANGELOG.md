0.1.24
-------------------

Fixes:
* Status code 409 is no longer retried by default.
* Status code 504 is now retried by default.
* Fixed bug when `AppItem.errors` have been structured incorrectly.
* Fixed the bug when an incorrect version of the `urllib3` was used.

Changes:
* `toloka.client.filters.Rating` was removed according to changes in Toloka API.
* All time data now have a UTC timezone by default (instead of a local timezone).

Streaming improvements:
* `toloka.streaming.Pipeline` now supports "gentle shutdown": the first SIGINT received will force the `Pipeline` to process all observers in the current iteration and then exit. On the second SIGINT received, the `Pipeline` will be interrupted (warning: this may lead to errors such as incorrect saved observers states).
* `toloka.streaming.Pipeline` now supports registering new observers during execution.
* Observers now support `delete`, `disable`, and `enable` methods: these methods change the target Observer state such that `toloka.streaming.Pipeline` handles it accordingly.

Other improvements:
* Added [MapView](https://toloka.ai/en/docs/toloka-kit/reference/toloka.client.project.template_builder.view.MapViewV1) Template Builder component.

0.1.23
-------------------
Python versions support:
* Python 3.10 support added
* Python 3.6 support dropped

Improvements:
* Added native support for verfied language skills
* Added native support for map provider's selection for pedestrian tasks in `AssignmentsIssuingViewConfig`
* Improved default status code dependent retry policies
* Requests originated from `toloka.streaming` or `toloka.metrics` are now marked with additional headers. This makes it easier for us to collect these features' usage statistics
* Annotations now use `urllib3` instead of weird `requests.packages.urllib3`
* Actualized outdated docstrings in `toloka.client.user_bonus`


0.1.22
-------------------
Fixes:
* Fixed uninitialized `start_soon`. See https://github.com/Toloka/toloka-kit/issues/48
* New `metrics` example


0.1.21 [YANKED]
-------------------
Fixes:
* Fixed maximum recursion depth exceptions
* Fixed `download_attachment`


0.1.20 [YANKED]
-------------------
Yanked due to issues found in retries functionality:
* Might raise maximum recursion depth exceptions
* Breaks `download_attachment`
Fixed in `toloka-kit==0.1.21`

Features:
* Retries should work not only while establishing connection to server but also when transfering data
* Added functional tests against production environment
* Fixed `TemplateBuilder` structure method issue with attributes annotated by `ListBaseComponent`
* TolokaClient method names are passed in request headers. This allows usage analytics for complex features such as `clone_project` or `get_assignments` that call subsequent TolokaClient methods.
* Now you can track 11 metric types from Toloka with minimal latency.

* AsyncTolokaClient introduced (experimental)
* Streaming state storage introduced (experimental)

0.1.19
-------------------
* Added `from_json` and `to_json` convenience functions to `BaseTolokaObject`
* Added docstrings for Toloka App API client part
* Supported classes with `async def __call__(...)` as streaming handlers
* `inherit_docstrings` decorator preserves `__init__` positional arguments ordering
* `TolokaClient` is now pickleable

0.1.18
-------------------
* Fixed an exceptions caused by returning status 204 with an empty body from API
* Fixed several bugs in toloka apps methods

0.1.17
-------------------
* Reverted from `PreloadingHTTPAdapter` to `HTTPAdapter`
* Fixed `get_app_items()` signature

0.1.16 [YANKED]
-------------------
* Added methods to use toloka apps
* Used `PreloadingHTTPAdapter` instead of `HTTPAdapter`

0.1.15
-------------------
* Downgraded attrs dependency from  `attrs>=21.2.0` to `attrs>=20.3.0`. See https://github.com/Toloka/toloka-kit/issues/37
* Cursor states are now updated after all callbecks are run successfully (toloka.straming)
* String values passed for Enum-annotated arguments are now automatically converted to Enums

0.1.14
-------------------

* `toloka.client` objects are not serializable
* Metrics are introduced


0.1.13
-------------------
* Streaming library to build pipelines
* Examples refactoring

0.1.12
-------------------
* Added new template builder components
* Added the ability to translate project title and description into multiple languages
* ExtendableStrEnum class has been added for forward compatibility with new enumeration keys

0.1.11
-------------------
* Added new `TemplateBuilder` components
* Deleted `name` from `UserSkillSearchRequest`
* Passing `Retry` object into `TolokaClient.retries` is now deprecated. Use new `TolokaClient.retryer_factory` argument instead.
* Added `__all__` to stub files
* Fixed an exception raising when opening an open pool
* Fixed `TemplateBuilder` view-components bug with the disappearance of the `hint`, `label` and `validation` fields in `0.1.10` version.

0.1.10 [YANKED]
-------------------
* `TemplateBuilder` components now support positional arguments
* Added `readonly` flag to attributes
* Added `ACCEPT_AFTER_REJECT` value to ` AssessmentEvent.Type`
* Added `assignment_id` attribute to `UserBonusSearchRequest`
* Improved stub files formatting

0.1.9
-------------------
* Improved support by static analyzers
* Added default value for `Pool.defaults` attribute
* Added default value 0 for `real_tasks_count`, `golden_tasks_count`, `training_tasks_count` in `MixerConfig`
* Added default value `AUTOMATED` for `Project.assignments_issuing_type` attribute
* Simplified `TolokaPluginV1`' interface by expanding `layout` attribute
* Simplified `TemplateBuilderViewSpec`'s interface by expanding `config` attribute
* Fixed an issue with `TemplateBuilder` config displayed in one line in Toloka's web interface
* `City`, `Languages`, `RegionByPhone` and `RegionByIp` filters now have `include` and `exclude`. Thix methods will eventually replace misleading `in_` and `not_in` method names. As for now, all variants are available for backward compatibility
* Retry Toloka quotas. Minute quotas are retried by default. And you can turn on the retrying of hourly and daily quotas.


0.1.8
-------------------
* Added `get_aggregated_solutions` method
* Supported webhooks related methods
* Tracebacks in expanded methods do not show confusing TypeError as an original exception


0.1.7
-------------------
* Fixed error on ARRAY_JSON typed fields specs structuring


0.1.6
-------------------
* Improved docstrings
* Supported list of statuses as valid argument for `get_assignments` and `get_message_threads`
* Fixed `help` on filter classes with overlloaded `__eq__`
* Added `YandexDiskProxyHelperV1` component for template builder
* TolokaClient can now be created with url
* Added `__all__` for modules
* Created objects' urls are now logged under INFO level, if possible

0.1.5
-------------------
Fixing issues with `create_tasks` and `create_task_suites`

0.1.4 [YANKED]
-------------------
* Implemented a `clone_project` method
* Deserialization should not fail on unknown enum values or unexpected value types anymore
* Some functions that used to return an Operation object now wait for operations to end and return a more usefull output. For example, `clone_pool` now returns an instance of Pool representing a newly created pool. If you want the old behaviour please use `*_async` versions of the methods. The list of affected methods:
  * archive_pool
  * archive_project
  * archive_training
  * clone_pool
  * clone_training
  * close_pool
  * close_pool_for_update
  * close_training
  * open_pool
  * open_training
* `create_tasks` and `create_task_suites` methods now use their async versions under the hood. This significantly reduces cases when TimeoutError is raised but the data is actually uploaded
* Added minimal attrs version
* Added WEARABLE_COMPUTER to DeviceCategory enum
* Fixed current_location naming in CoordinatesSpec

0.1.3
-------------------
* Added support for trainings
* Introduced `get_assignments_df` method

0.1.2
-------------------
* Introduced template builder support
* Introduced `get_analytics` method
* Sensitive values such as rewards and bonuses are now represented as decimal.Decimal
