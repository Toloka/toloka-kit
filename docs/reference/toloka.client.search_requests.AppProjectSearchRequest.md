# AppProjectSearchRequest
`toloka.client.search_requests.AppProjectSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/search_requests.py#L952)

```python
AppProjectSearchRequest(
    self,
    app_id: Optional[str] = None,
    parent_app_project_id: Optional[str] = None,
    status: Optional[AppProject.Status] = None,
    after_id: Optional[str] = None,
    scope: Optional[Scope] = None,
    requester_ids: Union[str, List[str], None] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    name_lt: Optional[str] = None,
    name_lte: Optional[str] = None,
    name_gt: Optional[str] = None,
    name_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None
)
```

Parameters for searching App projects.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`app_id`|**Optional\[str\]**|<p>App ID that the projects belong to.</p>
`parent_app_project_id`|**Optional\[str\]**|<p>ID of the App project used for cloning. It&#x27;s specified only if you created an App project by cloning another App project. You can clone projects in the web version of Toloka.</p>
`status`|**Optional\[[AppProject.Status](toloka.client.app.AppProject.Status.md)\]**|<p>project status.</p>
`after_id`|**Optional\[str\]**|<p>ID of the project used for cursor pagination.</p>
`scope`|**Optional\[[Scope](toloka.client.search_requests.AppProjectSearchRequest.Scope.md)\]**|<p>projects created by a specified range of requesters:<ul><li>MY - Only by me;</li><li>COMPANY - By anyone from the company;</li><li>REQUESTER_LIST - By requesters with the specified IDs.</li></ul></p>
`requester_ids`|**Optional\[List\[str\]\]**|<p>List of requester IDs separated by a comma, for scope = REQUESTER_LIST.</p>
`id_gt`|**Optional\[str\]**|<p>projects with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>projects with an ID greater than or equal to the specified value.</p>
`id_lt`|**Optional\[str\]**|<p>projects with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>projects with an ID less than or equal to the specified value.</p>
`name_gt`|**Optional\[str\]**|<p>projects with a name lexicographically greater than the specified value.</p>
`name_gte`|**Optional\[str\]**|<p>projects with a name lexicographically greater than or equal to the specified value.</p>
`name_lt`|**Optional\[str\]**|<p>projects with a name lexicographically less than the specified value.</p>
`name_lte`|**Optional\[str\]**|<p>projects with a name lexicographically less than or equal to the specified value.</p>
`created_gt`|**Optional\[datetime\]**|<p>projects created after the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_gte`|**Optional\[datetime\]**|<p>projects created after or on the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lt`|**Optional\[datetime\]**|<p>projects created before the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
`created_lte`|**Optional\[datetime\]**|<p>projects created before or on the specified date. The date is specified in UTC in ISO 8601 format: YYYY-MM-DDThh:mm:ss[.sss].</p>
