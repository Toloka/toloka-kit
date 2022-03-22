# run_dash
`toloka.metrics.jupyter_dashboard.DashBoard.run_dash` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/metrics/jupyter_dashboard.py#L44)

```python
run_dash(
    self,
    mode: str = 'inline',
    height: int = None,
    host: str = '127.0.0.1',
    port: str = '8050'
)
```

Starts dashboard. Starts server for online updating charts.


You can stop it, by calling 'stop_dash()' for the same dashboard instance.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`mode`|**str**|<p>Same as &#x27;mode&#x27; in jupyter_dash.JupyterDash().run_server(). Defaults to &#x27;inline&#x27;.</p>
`height`|**int**|<p>If you don&#x27;t want auto-computed height. Defaults to None - auto-compute.</p>
`host`|**str**|<p>Host for server. Defaults to &#x27;127.0.0.1&#x27;.</p>
`port`|**str**|<p>Port fo server. Defaults to &#x27;8050&#x27;.</p>
