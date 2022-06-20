# create_skill
`toloka.client.TolokaClient.create_skill`

Creates a new Skill


You can send a maximum of 10 requests of this kind per minute and 100 requests per day.

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
`id`|**-**|<p>Skill ID. Read only field.</p>
`created`|**-**|<p>The UTC date and time when the skill was created. Read only field.</p>

* **Returns:**

  Created skill. With read-only fields.

* **Return type:**

  [Skill](toloka.client.skill.Skill.md)

**Examples:**

How to create a new skill.

```python
new_skill = toloka_client.create_skill(
    name='Area selection of road signs',
    public_requester_description={
        'EN': 'Performer is annotating road signs',
        'FR': "L'exécuteur marque les signaux routier",
    },
)
print(new_skill.id)
```
