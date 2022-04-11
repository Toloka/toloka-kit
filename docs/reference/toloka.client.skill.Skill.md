# Skill
`toloka.client.skill.Skill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/skill.py#L10)

```python
Skill(
    self,
    *,
    name: Optional[str] = None,
    private_comment: Optional[str] = None,
    hidden: Optional[bool] = None,
    skill_ttl_hours: Optional[int] = None,
    training: Optional[bool] = None,
    public_name: Optional[Dict[str, str]] = None,
    public_requester_description: Optional[Dict[str, str]] = None,
    id: Optional[str] = None,
    created: Optional[datetime] = None
)
```

A skill is an assessment of some aspect of a user's responses (a number from 0 to 100)


Skill is a general grouping entity, for example "image annotation", which is created once and then used.
To set the Skill value for a specific performer, use UserSkill.
You can set up skill calculation in a quality control rule, or manually set the skill level for a user.
You can use skills to select users who perform pool tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`name`|**Optional\[str\]**|<p>Skill name.</p>
`private_comment`|**Optional\[str\]**|<p>Comments on the skill (only visible to the requester).</p>
`hidden`|**Optional\[bool\]**|<p>Access to information about the skill (the name and value) for users:<ul><li>True - Closed. Default behaviour.</li><li>False - Opened.</li></ul></p>
`skill_ttl_hours`|**Optional\[int\]**|<p>The skill&#x27;s &quot;time to live&quot; after the last update (in hours). The skill is removed from the user&#x27;s profile if the skill level hasn&#x27;t been updated for the specified length of time.</p>
`training`|**Optional\[bool\]**|<p>Whether the skill is related to a training pool:<ul><li>True - The skill level is calculated from training pool tasks.</li><li>False - The skill isn&#x27;t related to a training pool.</li></ul></p>
`public_name`|**Optional\[Dict\[str, str\]\]**|<p>Skill name for other users. You can provide a name in several languages (the message will come in the user&#x27;s language).</p>
`public_requester_description`|**Optional\[Dict\[str, str\]\]**|<p>Skill description text for other users. You can provide text in several languages (the message will come in the user&#x27;s language).</p>
`id`|**Optional\[str\]**|<p>Skill ID. Read only field.</p>
`created`|**Optional\[datetime\]**|<p>The UTC date and time when the skill was created. Read only field.</p>

**Examples:**

How to create new skill.

```python
segmentation_skill = toloka_client.create_skill(
    name='Area selection of road signs',
    public_requester_description={
        'EN': 'Performer is annotating road signs',
        'RU': 'Как исполнитель размечает дорожные знаки',
    },
)
print(segmentation_skill.id)
```

How to find skill.

```python
segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
if segmentation_skill:
    print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
else:
    print('Create new segmentation skill here')
```
