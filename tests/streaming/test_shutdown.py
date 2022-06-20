import asyncio
import attr
import datetime
import os
import pytest
import signal
import time
from concurrent import futures
from typing import Optional

from toloka.streaming import Pipeline
from toloka.streaming.storage import JSONLocalStorage
from toloka.util.async_utils import ComplexException


@pytest.fixture
def pid_file_path(tmp_path):
    return tmp_path / 'to-kill-sigint.pid'


@pytest.fixture
def storage_directory(tmp_path):
    dirname = tmp_path / 'storage_directory'
    dirname.mkdir()
    return dirname


OBSERVER_DURATION = 0.4


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

    def _get_unique_key(self):
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


def _run_pipeline(pid_file_path: str, dirname: str):
    pipeline, _, _ = _create_pipeline(dirname, 'observer-before-ctrl-c')
    pid = os.getpid()
    with open(pid_file_path, 'w') as file:
        file.write(str(pid))
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pipeline.run())


def _throw_sigint(pid_file_path: str, interrupt_after: float):
    time.sleep(interrupt_after)
    with open(pid_file_path) as file:
        pid = int(file.read())
    os.kill(pid, signal.SIGINT)


def test_gracefully_shutdown(pid_file_path, storage_directory):
    with futures.ProcessPoolExecutor() as executor:
        done, _ = futures.wait([executor.submit(_run_pipeline, pid_file_path, storage_directory),
                                executor.submit(_throw_sigint, pid_file_path, OBSERVER_DURATION / 2)])
        for task in done:
            error = task.exception()
            if error and not isinstance(error, futures.BrokenExecutor):
                raise error

    pipeline, observer, fail_observer = _create_pipeline(storage_directory, 'observer-after-ctrl-c')
    with pytest.raises(ComplexException):
        asyncio.new_event_loop().run_until_complete(pipeline.run())
    assert observer.injection.name == 'observer-before-ctrl-c'
    assert observer.injection.count == 1
    assert fail_observer.injection is None  # Only successful workers are saved.


LONG_WAIT_SECONDS = 10
SHORT_OBSERVER_DURATION = 0.1


def _run_long_sleeping_pipeline(pid_file_path: str):
    Pipeline.MIN_SLEEP_SECONDS = LONG_WAIT_SECONDS
    pipeline = Pipeline(period=datetime.timedelta(seconds=LONG_WAIT_SECONDS))
    pipeline.register(ObserverToInterrupt('short-observer', duration=SHORT_OBSERVER_DURATION))

    pid = os.getpid()
    with open(pid_file_path, 'w') as file:
        file.write(str(pid))
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pipeline.run())


def test_interrupt_sleeping(pid_file_path):
    start_time = time.time()

    with futures.ProcessPoolExecutor() as executor:
        done, _ = futures.wait([executor.submit(_run_long_sleeping_pipeline, pid_file_path),
                                executor.submit(_throw_sigint, pid_file_path, SHORT_OBSERVER_DURATION * 1.5)])
        for task in done:
            error = task.exception()
            if error and not isinstance(error, KeyboardInterrupt):
                raise error

    elapsed = time.time() - start_time
    assert elapsed < LONG_WAIT_SECONDS, elapsed
