import asyncio
import datetime
import os
import signal
import time
from multiprocessing import Process
from typing import Optional

import attr
import pytest
from toloka.streaming import Pipeline
from toloka.streaming.storage import JSONLocalStorage
from toloka.util.async_utils import ComplexException


@pytest.fixture
def storage_directory(tmp_path):
    dirname = tmp_path / 'storage_directory'
    dirname.mkdir()
    return dirname


OBSERVER_DURATION = 1


@attr.s
class ObserverToInterrupt:
    name: str = attr.ib()  # Has no impact on key here.
    duration: float = attr.ib(default=OBSERVER_DURATION)
    count: int = attr.ib(default=0)
    max_count: int = attr.ib(default=2)
    injection: Optional['ObserverToInterrupt'] = attr.ib(default=None, init=False)
    _should_resume: bool = attr.ib(default=True, init=False)

    async def __call__(self):
        self.count += 1
        await asyncio.sleep(self.duration)
        if self.count >= self.max_count:
            self._should_resume = False

    async def should_resume(self):
        return self._should_resume

    def get_unique_key(self):
        return f'some-uniq-key-for-{type(self).__name__}'

    def inject(self, other: 'ObserverToInterrupt') -> None:
        self.injection = other


class ObserverThatFails(ObserverToInterrupt):
    async def __call__(self):
        await super().__call__()
        raise ValueError('error-from-ObserverThatFails')


def _create_pipeline(dirname: str, observer_name: str):
    Pipeline.MIN_SLEEP_SECONDS = 0
    pipeline = Pipeline(storage=JSONLocalStorage(dirname=dirname), period=datetime.timedelta(seconds=OBSERVER_DURATION))
    observer = pipeline.register(ObserverToInterrupt(observer_name))
    fail_observer = pipeline.register(ObserverThatFails(observer_name))
    return pipeline, observer, fail_observer


def _run_pipeline(dirname: str):
    pipeline, _, _ = _create_pipeline(dirname, 'observer-before-ctrl-c')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pipeline.run())


def _throw_sigint(pid: int, interrupt_after: float):
    time.sleep(interrupt_after)
    os.kill(pid, signal.SIGINT)


def test_gracefully_shutdown(storage_directory):
    pipeline_process = Process(target=_run_pipeline, args=(storage_directory,))
    pipeline_process.start()
    killer_process = Process(target=_throw_sigint, args=(pipeline_process.pid, OBSERVER_DURATION / 2))
    killer_process.start()
    pipeline_process.join()
    killer_process.join()

    assert pipeline_process.exitcode == 1
    assert killer_process.exitcode == 0

    pipeline, observer, fail_observer = _create_pipeline(storage_directory, 'observer-after-ctrl-c')
    with pytest.raises(ComplexException):
        asyncio.new_event_loop().run_until_complete(pipeline.run())
    assert observer.injection.name == 'observer-before-ctrl-c'
    assert observer.injection.count == 1
    assert fail_observer.injection is None  # Only successful workers are saved.


LONG_WAIT_SECONDS = 10
SHORT_OBSERVER_DURATION = 0.1


def _run_long_sleeping_pipeline():
    Pipeline.MIN_SLEEP_SECONDS = LONG_WAIT_SECONDS
    pipeline = Pipeline(period=datetime.timedelta(seconds=LONG_WAIT_SECONDS))
    pipeline.register(ObserverToInterrupt('short-observer', duration=SHORT_OBSERVER_DURATION))
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pipeline.run())


def test_interrupt_sleeping():
    start_time = time.time()

    pipeline_process = Process(target=_run_long_sleeping_pipeline)
    pipeline_process.start()
    killer_process = Process(target=_throw_sigint, args=(pipeline_process.pid, OBSERVER_DURATION / 2))
    killer_process.start()
    pipeline_process.join()
    killer_process.join()

    assert pipeline_process.exitcode == 1
    assert killer_process.exitcode == 0

    elapsed = time.time() - start_time
    assert elapsed < LONG_WAIT_SECONDS, elapsed
