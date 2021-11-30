# TolokaClient
`toloka.client.TolokaClient`

```
TolokaClient(
    self,
    token: str,
    environment: Union[Environment, str, None] = None,
    retries: Union[int, Retry] = 3,
    timeout: Union[float, Tuple[float, float]] = ...,
    url: Optional[str] = None,
    retry_quotas: Union[List[str], str, None] = 'MIN',
    retryer_factory: Optional[Callable[[], Retry]] = None
)
```

Class that implements interaction with [Toloka API](https://yandex.com/dev/toloka/doc/concepts/about.html).


Objects of other classes are created and modified only in memory of your computer.
You can transfer information about these objects to Toloka only by calling one of the `TolokaClient` methods.

For example, creating an instance of `Project` class will not add a project to Toloka right away. It will create a `Project` instance in your local memory.
You need to call the `TolokaClient.create_project` method and pass the created project instance to it.
Likewise, if you read a project using the `TolokaClient.get_project` method, you will get an instance of `Project` class.
But if you change some parameters in this object manually in your code, it will not affect the existing project in Toloka.
Call `TolokaClient.update_project` and pass the `Project` to apply your changes.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`token`|**str**|<p>Your OAuth token for Toloka. You can learn more about how to get it [here](https://yandex.com/dev/toloka/doc/concepts/access.html#access__token)</p>
`environment`|**Union\[[Environment](toloka.client.TolokaClient.Environment.md), str, None\]**|<p>There are two environments in Toloka:<ul><li>`SANDBOX` – [Testing environment](https://sandbox.toloka.yandex.com) for Toloka requesters. You can test complex projects before starting them on real performers. Nobody will see your tasks, and it&#x27;s free.</li><li>`PRODUCTION` – [Production environment](https://toloka.yandex.com) for Toloka requesters. You spend money there and get the results. You need to register in each environment separately. OAuth tokens are generated in each environment separately too. </li></ul></p><p>Default value: `None`.</p>
`retries`|**Union\[int, Retry\]**|<p>Retry policy for failed API requests. Possible values:<ul><li>`int` – The number of retries for all requests. In this case, the retry policy is created automatically.</li><li>`Retry` object – Deprecated type. Use `retryer_factory` parameter instead. </li></ul></p><p>Default value: `3`.</p>
`timeout`|**Union\[float, Tuple\[float, float\]\]**|<p>Number of seconds that [Requests library](https://docs.python-requests.org/en/master) will wait for your client to establish connection to a remote machine. Possible values:<ul><li>`float` – Single value for both connect and read timeouts.</li><li>`Tuple[float, float]` – Tuple sets the values for connect and read timeouts separately.</li><li>`None` – Set the timeout to `None` only if you are willing to wait the [Response](https://docs.python-requests.org/en/master/api/#requests.Response) for unlimited number of seconds. </li></ul></p><p>Default value: `10.0`.</p>
`url`|**Optional\[str\]**|<p>Set a specific URL instead of Toloka environment. May be useful for testing purposes. You can only set one parameter – either `url` or `environment`, not both of them. </p><p>Default value: `None`.</p>
`retry_quotas`|**Union\[List\[str\], str, None\]**|<p>List of quotas that must be retried. Set `None` or pass an empty list for not retrying any quotas. If you specified the `retries` as `Retry` instance, you must set this parameter to `None`. Possible values:<ul><li>`MIN` - Retry minutes quotas.</li><li>`HOUR` - Retry hourly quotas. This means that the program just sleeps for an hour.</li><li>`DAY` - Retry daily quotas. We do not recommend retrying these quotas. </li></ul></p><p>Default value: `MIN`.</p>
`retryer_factory`|**Optional\[Callable\[\[\], Retry\]\]**|<p>Factory that creates `Retry` object. Fully specified retry policy that will apply to all requests. </p><p>Default value: `None`.</p>

**Examples:**

How to create `TolokaClient` instance and make your first request to Toloka.

```python
your_oauth_token = input('Enter your token:')
toloka_client = toloka.TolokaClient(your_oauth_token, 'PRODUCTION')  # Or switch to 'SANDBOX' environment
```

**Note**: `toloka_client` instance will be used to pass all API calls later on.
## Methods summary

| Method | Description |
| :------| :-----------|
[accept_assignment](toloka.client.TolokaClient.accept_assignment.md)| Marks one assignment as accepted
[add_message_thread_to_folders](toloka.client.TolokaClient.add_message_thread_to_folders.md)| Adds a message chain to one or more folders ("unread", "important" etc.)
[aggregate_solutions_by_pool](toloka.client.TolokaClient.aggregate_solutions_by_pool.md)| Starts aggregation of solutions in the pool
[aggregate_solutions_by_task](toloka.client.TolokaClient.aggregate_solutions_by_task.md)| Starts aggregation of solutions to a single task
[archive_app_project](toloka.client.TolokaClient.archive_app_project.md)| Archiving the project.
[archive_pool](toloka.client.TolokaClient.archive_pool.md)| Sends pool to archive
[archive_pool_async](toloka.client.TolokaClient.archive_pool_async.md)| Sends pool to archive, asynchronous version
[archive_project](toloka.client.TolokaClient.archive_project.md)| Sends project to archive
[archive_project_async](toloka.client.TolokaClient.archive_project_async.md)| Sends project to archive, asynchronous version
[archive_training](toloka.client.TolokaClient.archive_training.md)| Sends training to archive
[archive_training_async](toloka.client.TolokaClient.archive_training_async.md)| Sends training to archive, asynchronous version
[clone_pool](toloka.client.TolokaClient.clone_pool.md)| Duplicates existing pool
[clone_pool_async](toloka.client.TolokaClient.clone_pool_async.md)| Duplicates existing pool, asynchronous version
[clone_project](toloka.client.TolokaClient.clone_project.md)| Synchronously clones the project, all pools and trainings
[clone_training](toloka.client.TolokaClient.clone_training.md)| Duplicates existing training
[clone_training_async](toloka.client.TolokaClient.clone_training_async.md)| Duplicates existing training, asynchronous version
[close_pool](toloka.client.TolokaClient.close_pool.md)| Stops distributing tasks from the pool
[close_pool_async](toloka.client.TolokaClient.close_pool_async.md)| Stops distributing tasks from the pool, asynchronous version
[close_pool_for_update](toloka.client.TolokaClient.close_pool_for_update.md)| Closes pool for update
[close_pool_for_update_async](toloka.client.TolokaClient.close_pool_for_update_async.md)| Closes pool for update, asynchronous version
[close_training](toloka.client.TolokaClient.close_training.md)| Stops distributing tasks from the training
[close_training_async](toloka.client.TolokaClient.close_training_async.md)| Stops distributing tasks from the training, asynchronous version
[compose_message_thread](toloka.client.TolokaClient.compose_message_thread.md)| Sends message to performer
[create_app_batch](toloka.client.TolokaClient.create_app_batch.md)| Creating a new batch.
[create_app_item](toloka.client.TolokaClient.create_app_item.md)| Adding a new work item.
[create_app_items](toloka.client.TolokaClient.create_app_items.md)| Creating a batch of new items.
[create_app_project](toloka.client.TolokaClient.create_app_project.md)| Creating a new App project.
[create_pool](toloka.client.TolokaClient.create_pool.md)| Creates a new pool
[create_project](toloka.client.TolokaClient.create_project.md)| Creates a new project
[create_skill](toloka.client.TolokaClient.create_skill.md)| Creates a new Skill
[create_task](toloka.client.TolokaClient.create_task.md)| Creates a new task
[create_task_suite](toloka.client.TolokaClient.create_task_suite.md)| Creates a new task suite
[create_task_suites](toloka.client.TolokaClient.create_task_suites.md)| Creates many task suites in pools
[create_task_suites_async](toloka.client.TolokaClient.create_task_suites_async.md)| Creates many task suites in pools, asynchronous version
[create_tasks](toloka.client.TolokaClient.create_tasks.md)| Creates many tasks in pools
[create_tasks_async](toloka.client.TolokaClient.create_tasks_async.md)| Creates many tasks in pools, asynchronous version
[create_training](toloka.client.TolokaClient.create_training.md)| Creates a new training
[create_user_bonus](toloka.client.TolokaClient.create_user_bonus.md)| Issues payments directly to the performer
[create_user_bonuses](toloka.client.TolokaClient.create_user_bonuses.md)| Creates many user bonuses
[create_user_bonuses_async](toloka.client.TolokaClient.create_user_bonuses_async.md)| Issues payments directly to the performers, asynchronously creates many user bonuses
[delete_user_restriction](toloka.client.TolokaClient.delete_user_restriction.md)| Unlocks existing restriction
[delete_user_skill](toloka.client.TolokaClient.delete_user_skill.md)| Drop specific UserSkill
[delete_webhook_subscription](toloka.client.TolokaClient.delete_webhook_subscription.md)| Drop specific webhook-subscription
[download_attachment](toloka.client.TolokaClient.download_attachment.md)| Downloads specific attachment
[find_aggregated_solutions](toloka.client.TolokaClient.find_aggregated_solutions.md)| Gets aggregated responses after the AggregatedSolutionOperation completes.
[find_app_batches](toloka.client.TolokaClient.find_app_batches.md)| Finds all batches in the App project that match certain rules.
[find_app_items](toloka.client.TolokaClient.find_app_items.md)| Finds all work items in the App project that match certain rules.
[find_app_projects](toloka.client.TolokaClient.find_app_projects.md)| Finds all App projects that match certain rules.
[find_apps](toloka.client.TolokaClient.find_apps.md)| Finds all Apps that match certain rules.
[find_assignments](toloka.client.TolokaClient.find_assignments.md)| Finds all assignments that match certain rules
[find_attachments](toloka.client.TolokaClient.find_attachments.md)| Finds all attachments that match certain rules
[find_message_threads](toloka.client.TolokaClient.find_message_threads.md)| Finds all message threads that match certain rules
[find_pools](toloka.client.TolokaClient.find_pools.md)| Finds all pools that match certain rules
[find_projects](toloka.client.TolokaClient.find_projects.md)| Finds all projects that match certain rules
[find_skills](toloka.client.TolokaClient.find_skills.md)| Finds all skills that match certain rules
[find_task_suites](toloka.client.TolokaClient.find_task_suites.md)| Finds all task suites that match certain rules
[find_tasks](toloka.client.TolokaClient.find_tasks.md)| Finds all tasks that match certain rules
[find_trainings](toloka.client.TolokaClient.find_trainings.md)| Finds all trainings that match certain rules
[find_user_bonuses](toloka.client.TolokaClient.find_user_bonuses.md)| Finds all user bonuses that match certain rules
[find_user_restrictions](toloka.client.TolokaClient.find_user_restrictions.md)| Finds all user restrictions that match certain rules
[find_user_skills](toloka.client.TolokaClient.find_user_skills.md)| Finds all user skills that match certain rules
[find_webhook_subscriptions](toloka.client.TolokaClient.find_webhook_subscriptions.md)| Finds all webhook-subscriptions that match certain rules
[get_aggregated_solutions](toloka.client.TolokaClient.get_aggregated_solutions.md)| Finds all aggregated responses after the AggregatedSolutionOperation completes
[get_analytics](toloka.client.TolokaClient.get_analytics.md)| Sends analytics queries, for example, to estimate the percentage of completed tasks in the pool
[get_app](toloka.client.TolokaClient.get_app.md)| Information about the App.
[get_app_batch](toloka.client.TolokaClient.get_app_batch.md)| Batch information.
[get_app_batches](toloka.client.TolokaClient.get_app_batches.md)| Finds all batches in the App project that match certain rules and returns them in an iterable object.
[get_app_item](toloka.client.TolokaClient.get_app_item.md)| Information about one work item.
[get_app_items](toloka.client.TolokaClient.get_app_items.md)| Finds all work items in the App project that match certain rules and returns them in an iterable object.
[get_app_project](toloka.client.TolokaClient.get_app_project.md)| Project information.
[get_app_projects](toloka.client.TolokaClient.get_app_projects.md)| Finds all App projects that match certain rules and returns them in an iterable object.
[get_apps](toloka.client.TolokaClient.get_apps.md)| Finds all Apps that match certain rules and returns them in an iterable object.
[get_assignment](toloka.client.TolokaClient.get_assignment.md)| Reads one specific assignment
[get_assignments](toloka.client.TolokaClient.get_assignments.md)| Finds all assignments that match certain rules and returns them in an iterable object
[get_assignments_df](toloka.client.TolokaClient.get_assignments_df.md)| Downloads assignments as pandas.DataFrame
[get_attachment](toloka.client.TolokaClient.get_attachment.md)| Gets attachment metadata without downloading it
[get_attachments](toloka.client.TolokaClient.get_attachments.md)| Finds all attachments that match certain rules and returns their metadata in an iterable object
[get_message_threads](toloka.client.TolokaClient.get_message_threads.md)| Finds all message threads that match certain rules and returns them in an iterable object
[get_operation](toloka.client.TolokaClient.get_operation.md)| Reads information about operation
[get_operation_log](toloka.client.TolokaClient.get_operation_log.md)| Reads information about validation errors and which task (or task suites) were created
[get_pool](toloka.client.TolokaClient.get_pool.md)| Reads one specific pool
[get_pools](toloka.client.TolokaClient.get_pools.md)| Finds all pools that match certain rules and returns them in an iterable object
[get_project](toloka.client.TolokaClient.get_project.md)| Reads one specific project
[get_projects](toloka.client.TolokaClient.get_projects.md)| Finds all projects that match certain rules and returns them in an iterable object
[get_requester](toloka.client.TolokaClient.get_requester.md)| Reads information about the customer and the account balance
[get_skill](toloka.client.TolokaClient.get_skill.md)| Reads one specific skill
[get_skills](toloka.client.TolokaClient.get_skills.md)| Finds all skills that match certain rules and returns them in an iterable object
[get_task](toloka.client.TolokaClient.get_task.md)| Reads one specific task
[get_task_suite](toloka.client.TolokaClient.get_task_suite.md)| Reads one specific task suite
[get_task_suites](toloka.client.TolokaClient.get_task_suites.md)| Finds all task suites that match certain rules and returns them in an iterable object
[get_tasks](toloka.client.TolokaClient.get_tasks.md)| Finds all tasks that match certain rules and returns them in an iterable object
[get_training](toloka.client.TolokaClient.get_training.md)| Reads one specific training
[get_trainings](toloka.client.TolokaClient.get_trainings.md)| Finds all trainings that match certain rules and returns them in an iterable object
[get_user_bonus](toloka.client.TolokaClient.get_user_bonus.md)| Reads one specific user bonus
[get_user_bonuses](toloka.client.TolokaClient.get_user_bonuses.md)| Finds all user bonuses that match certain rules and returns them in an iterable object
[get_user_restriction](toloka.client.TolokaClient.get_user_restriction.md)| Reads one specific user restriction
[get_user_restrictions](toloka.client.TolokaClient.get_user_restrictions.md)| Finds all user restrictions that match certain rules and returns them in an iterable object
[get_user_skill](toloka.client.TolokaClient.get_user_skill.md)| Gets the value of the user's skill
[get_user_skills](toloka.client.TolokaClient.get_user_skills.md)| Finds all user skills that match certain rules and returns them in an iterable object
[get_webhook_subscription](toloka.client.TolokaClient.get_webhook_subscription.md)| Get one specific webhook-subscription
[get_webhook_subscriptions](toloka.client.TolokaClient.get_webhook_subscriptions.md)| Finds all webhook-subscriptions that match certain rules and returns them in an iterable object
[open_pool](toloka.client.TolokaClient.open_pool.md)| Starts distributing tasks from the pool
[open_pool_async](toloka.client.TolokaClient.open_pool_async.md)| Starts distributing tasks from the pool, asynchronous version
[open_training](toloka.client.TolokaClient.open_training.md)| Starts distributing tasks from the training
[open_training_async](toloka.client.TolokaClient.open_training_async.md)| Starts distributing tasks from the training, asynchronous version
[patch_assignment](toloka.client.TolokaClient.patch_assignment.md)| Changes status and comment on assignment
[patch_pool](toloka.client.TolokaClient.patch_pool.md)| Changes the priority of the pool issue
[patch_task](toloka.client.TolokaClient.patch_task.md)| Changes the task overlap
[patch_task_overlap_or_min](toloka.client.TolokaClient.patch_task_overlap_or_min.md)| Stops issuing the task
[patch_task_suite](toloka.client.TolokaClient.patch_task_suite.md)| Changes the task suite overlap or priority
[patch_task_suite_overlap_or_min](toloka.client.TolokaClient.patch_task_suite_overlap_or_min.md)| Stops issuing the task suites
[reject_assignment](toloka.client.TolokaClient.reject_assignment.md)| Marks one assignment as rejected
[remove_message_thread_from_folders](toloka.client.TolokaClient.remove_message_thread_from_folders.md)| Deletes a message chain from one or more folders ("unread", "important" etc.)
[reply_message_thread](toloka.client.TolokaClient.reply_message_thread.md)| Replies to a message in thread
[set_user_restriction](toloka.client.TolokaClient.set_user_restriction.md)| Closes the performer's access to one or more projects
[set_user_skill](toloka.client.TolokaClient.set_user_skill.md)| Sets the skill value to the performer
[start_app_batch](toloka.client.TolokaClient.start_app_batch.md)| Start processing the batch.
[unarchive_app_project](toloka.client.TolokaClient.unarchive_app_project.md)| Unarchiving the project.
[update_pool](toloka.client.TolokaClient.update_pool.md)| Makes changes to the pool
[update_project](toloka.client.TolokaClient.update_project.md)| Makes changes to the project
[update_skill](toloka.client.TolokaClient.update_skill.md)| Makes changes to the skill
[update_training](toloka.client.TolokaClient.update_training.md)| Makes changes to the training
[upsert_webhook_subscriptions](toloka.client.TolokaClient.upsert_webhook_subscriptions.md)| Creates (upsert) many webhook-subscriptions.
[wait_operation](toloka.client.TolokaClient.wait_operation.md)| Waits for the operation to complete, and return it
