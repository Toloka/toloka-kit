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
