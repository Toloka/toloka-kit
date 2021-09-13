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

0.1.10
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

0.1.4
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
