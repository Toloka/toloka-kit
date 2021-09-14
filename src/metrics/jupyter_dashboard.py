"""Classes for creating online dashboards with tolokas metrics in jupyter notebooks.

For usage examples see DashBoard.
"""

__all__ = [
    'DashBoard',
    'Chart',
]

import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from collections import namedtuple
import datetime
import logging
import math
import sys
from typing import Dict, List, Optional, Union
import uuid

if sys.version_info[:2] >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

from .metrics import BaseMetric

logger = logging.getLogger(__name__)


class Chart:
    """One chart on the dashboard. Could include several metrics.
    If you want to draw really cool chart that displays several metrics in the same coordinates.

    Args:
        name: The header for this chart. Could be None, Chart create name from the first metric.
        metrics: List of metrics, that will be displayed on this chart (in the same coordinates).

    Example:
        How to display all submitted and accepted answers from some pool and its checking pool, in one chart.

        >>> Chart(
        >>>     'Answers count',
        >>>     [
                    metrics.AssignmentsInPool('123', submitted_name='submitted in 123', accepted_name='accepted in 123', toloka_client=client1),
                    metrics.AssignmentsInPool('456', submitted_name='submitted in 456', accepted_name='accepted in 456', toloka_client=client2),
                ]
        >>> )
    """
    LineStats = namedtuple('LineStats', ['x', 'y', 'name'])

    _name: str
    metrics: List[BaseMetric]
    _id: str
    _lines: Dict[str, LineStats]  # {'line_id': ([x_times], [y_values], 'line name')}

    def __init__(self, name: Optional[str], metrics: List[BaseMetric]):
        self._name = name
        self._id = str(uuid.uuid4())
        self.metrics = []
        for i, element in enumerate(metrics):
            if not isinstance(element, BaseMetric):
                raise TypeError(f'{i} element in metrics must be an instance of toloka.metrics.BaseMetric, now it\'s {type(element)}')
            self.metrics.append(element)

        self._lines = {
            self._get_unique_name(name, metric): Chart.LineStats([], [], name)
            for metric in metrics
            for name in metric.get_line_names()
        }

    def _get_unique_name(self, name: str, metric: BaseMetric) -> str:
        return f'{name}-{id(metric)}'

    def update_metrics(self):
        """Gathers all metrics, and stores them in lines.
        """
        for metric in self.metrics:
            for name, points in metric.get_lines().items():
                x_list, y_list, _ = self._lines[self._get_unique_name(name, metric)]
                for x, y in points:
                    x_list.append(x)
                    y_list.append(y)

    def create_figure(self) -> go.Figure:
        """Create figure for this chart. Called at each step.

        Returns:
            Exactly one Figure for this chart.
        """

        # For cases then we create Chart from raw Metric in DashBoard.
        # In this case, it's only one metric in metrics.
        if self._name is None:
            self._name = self.metrics[0].beautiful_name

        figure = go.Figure()
        for x_points, y_points, line_name  in self._lines.values():
            figure.add_trace(
                go.Scatter(
                    x=x_points if x_points else [datetime.datetime.utcnow()],
                    y=y_points if y_points else [0],
                    name=line_name,
                    mode='lines',
                    hovertemplate='%{y} at %{x|%H:%M:%S}',
                )
            )

        figure.update_layout(
            title={
                'text': self._name,
                'xanchor': 'center',
                'yanchor': 'top',
                'y': 0.98,
                'x': 0.5,
            },
            showlegend=True,
            legend={
                'orientation': "h",
                'yanchor': "bottom",
                'y': -0.5,
                'xanchor': "center",
                'x': 0.5,
            },
            margin={'t': 0, 'r': 0, 'l': 0, 'b': 0},
            xaxis={'anchor': 'y', 'domain': [0.0, 1.0]},
            yaxis={'anchor': 'x', 'domain': [0.0, 1.0]},
            height=200,
        )
        return figure


class DashBoard:
    """Toloka dashboard with metrics. Only for jupyter.

    Args:
        metrics: List of metrics or charts, that will be displayed on the dashboard.
            Each element will be displayed in a separate chart (coordinates).
            If you want to draw several metrics in one coordinates, wrap it into an instance of the class Chart.
        header: Your pretty header for this dashboard.
        update_seconds: Count of seconds between dash updates.
        min_time_range: The minimum time range for all charts.
        max_time_range: The maximum time range for all charts. If you have more data, you will see only the last range on charts.

    Examples:
        How to create online dashboard in jupyter.

        >>> import toloka.metrics as metrics
        >>> from toloka.metrics.jupyter_dashboard import Chart, DashBoard
        >>> import toloka.client as toloka
        >>> toloka_client = toloka.TolokaClient(oauth_token, 'PRODUCTION')
        >>> new_dash = DashBoard(
        >>>     [
        >>>         metrics.Balance(),
        >>>         metrics.AssignmentsInPool('123'),
        >>>         metrics.AssignmentEventsInPool('123', submitted_name='submitted', join_events=True),
        >>>         Chart(
        >>>             'Manualy configured chart',
        >>>             [metrics.AssignmentsInPool('123'), metrics.AssignmentsInPool('345'),]
        >>>         )
        >>>     ],
        >>>     header='My cool dash',
        >>> )
        >>> metrics.bind_client(new_dash.metrics, toloka_client)
        >>> # Then in new cell:
        >>> new_dash.run_dash()
        >>> # If you want to stops it:
        >>> new_dash.stop_dash()
        ...
    """

    _charts: Dict[str, Chart]
    _dashboard: JupyterDash
    _host: Optional[str] = None
    _port: Optional[str] = None
    _time_from: Optional[datetime.datetime] = None
    _time_delta: int = 0
    _min_time_range: datetime.timedelta
    _max_time_range: datetime.timedelta
    _update_seconds: int

    CHART_STYLE_TEMPLATE = {'width': '48%', 'display': 'inline-block', 'padding': '0px 0px'}

    def __init__(
        self,
        metrics: List[Union[BaseMetric, Chart]],
        header='Toloka metrics dashboard',
        update_seconds: int = 10,
        min_time_range: datetime.timedelta = datetime.timedelta(minutes=1),
        max_time_range: datetime.timedelta = datetime.timedelta(hours=4),
    ):
        if update_seconds < 10:
            logger.warning('It\'s not recommended to set update_seconds less than 10.')
        self._update_seconds = update_seconds
        self._min_time_range = min_time_range
        self._max_time_range = max_time_range
        self._charts = {}
        for i, element in enumerate(metrics):
            if isinstance(element, BaseMetric):
                chart = Chart(None, [element])
                self._charts[chart._id] = chart
            elif isinstance(element, Chart):
                self._charts[element._id] = element
            else:
                raise TypeError(f'{i} element in metrics must be an instance of toloka.metrics.BaseMetric or toloka.metrics.jupyter_dashboard.Chart, now it\'s {type(element)}')

        # creates and configure dashboard
        self._dashboard = JupyterDash(
            f'Toloka dashboard {str(uuid.uuid4())}',
            external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
        )
        html_list = []
        html_list.append(html.H1(header))  # TODO: toloka icon
        html_list.append(dcc.Interval(id='interval-component', interval=self._update_seconds*1000, n_intervals=0))
        for i, chart_id in enumerate(self._charts.keys()):
            # margin format 'top right down left'
            # first row has zero top margin, all other 20px
            # all left charts(0, 2, 4, etc.) has 2% right margin
            # all charts has zero bottom margin
            # all right charts(1, 3, 5, etc.) has 2% left margin
            margin = f'{20 if i >= 2 else 0}px {2 if i%2 == 0 else 0}% 0px {2 if i%2 != 0 else 0}%'
            if i >= 2 and i % 2 == 0:
                html_list.append(html.Br())
            html_list.append(
                html.Div(
                    [dcc.Graph(id=chart_id)],
                    style={**DashBoard.CHART_STYLE_TEMPLATE, 'margin': margin}
                )
            )
        self._dashboard.layout = html.Div(html_list)

        # creates the callback that will update graphs
        ouput_list = [Output(chart_id, 'figure') for chart_id in self._charts.keys()]
        self._dashboard.callback(*ouput_list, Input('interval-component', 'n_intervals'))(self.update_charts)

    @cached_property
    def metrics(self) -> List[BaseMetric]:
        res_list = []
        for chart in self._charts.values():
            res_list = res_list + chart.metrics
        return res_list

    def update_charts(self, n_intervals: int):
        """Redraws all charts on each iteration

        Args:
            n_intervals (int): inner parameter that don't used right now

        Returns:
            Union[plotly.graph_objects.Figure(), List[plotly.graph_objects.Figure()]]: all new Figure's.
                Must have the same length on each iteration.
        """
        # TODO: Maybe it's worth updating only the part of the graphs that we managed to calculate,
        # and next time we should update it further.
        # Because many metrics easily take at least 1 second, for the simplest operations
        now = datetime.datetime.utcnow()
        if self._time_from is None:
            self._time_from = now
        time_from = self._time_from
        time_to = now
        if time_to - time_from < self._min_time_range:
            time_to = time_from + self._min_time_range + datetime.timedelta(seconds=self._update_seconds)
        elif time_to - time_from > self._max_time_range:
            time_from = time_to - self._max_time_range

        figures = []
        for chart in self._charts.values():
            chart.update_metrics()
            # TODO: right now all times in utc. May be we can auto-set user current time-zone.
            new_figure = chart.create_figure()
            new_figure.update_layout(xaxis_range=[time_from, time_to])
            figures.append(new_figure)
        return figures if len(figures) > 1 else figures[0]

    def run_dash(self, mode='inline', height=None, host='127.0.0.1', port='8050'):
        """Starts dashboard. Starts server for online updating charts.

        You can stop it, by calling 'stop_dash()' for the same dashboard instance.

        Args:
            mode: Same as 'mode' in jupyter_dash.JupyterDash().run_server(). Defaults to 'inline'.
            height: If you don't want auto-computed height. Defaults to None - auto-compute.
            host: Host for server. Defaults to '127.0.0.1'.
            port: Port fo server. Defaults to '8050'.
        """
        self.stop_dash()
        if height is None:
            rows = math.ceil(len(self._charts) / 2)
            height = 220*rows + 100
        self._host = host
        self._port = port
        self._dashboard.run_server(mode=mode, height=height, host=host, port=port)

    def stop_dash(self):
        """Stops server. And stops updating dashboard.
        """
        if self._host is not None and self._port is not None:
            self._dashboard._terminate_server_for_port(self._host, self._port)
        self._host = None
        self._port = None

    def __del__(self):
        self.stop_dash()
