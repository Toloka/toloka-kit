import attr
import json
import time
import os
import pytest
from concurrent import futures
from io import BytesIO
from typing import Dict, List
from toloka.streaming.storage import FileLocker, JSONLocalStorage, S3Storage


@pytest.fixture
def obj_to_store():
    return {'a': 1, 'b': 2.2, 'c': ['3', (4, None, ('абв', 'あ'))]}


@pytest.fixture
def base_encoded():
    return 'HxvmYIAcEI16m7012L0lKUz3SaUqs4fAEdgXLffHej4eWdU_o5IbnFnn5F3nTMXRJhha07_NuV_HdDHIaWDWHQ'


@pytest.fixture
def key_encoded():
    return 'jixChDQEF2aMpModrR2VhYZ1iAlAV701vUlA2-mlYlDdIoZFnxiclCEcaoocol5sg83irFeABVM3uPh63W4xBQ'


@pytest.fixture
def json_storage_result():
    return {
        "base_key": "some_pipeline_key",
        "key": "some_key",
        "value": "gASVOgAAAAAAAAB9lCiMAWGUSwGMAWKUR0ABmZmZmZmajAFjlF2UKIwBM5RLBE6MBtCw0LHQspSMA+OBgpSGlIeUZXUu",
        "meta": {}
    }


def check_stored_meta(meta):
    assert meta.pop('os_name')
    assert meta.pop('hostname')
    assert meta.pop('pid')
    assert meta.pop('py_version')
    assert meta.pop('pickle_version')
    assert meta.pop('toloka_kit_version')
    assert meta.pop('datetime')
    assert meta.pop('ts')


def test_json_storage(tmp_path, obj_to_store, base_encoded, key_encoded, json_storage_result):
    dirname = tmp_path / 'storage'
    dirname.mkdir()

    storage = JSONLocalStorage(dirname=dirname)
    storage.save('some_pipeline_key', {'some_key': obj_to_store})

    with open(dirname / f'JSONLocalStorage_{base_encoded}' / key_encoded) as file:
        stored = json.load(file)
        check_stored_meta(stored['meta'])
        assert json_storage_result == stored

    assert {'some_key': obj_to_store} == storage.load('some_pipeline_key', ['some_key', 'unknown_key'])


@pytest.mark.parametrize('lock_dirname', [None, 'lock_storage'])
def test_store_with_lock(tmp_path, obj_to_store, base_encoded, key_encoded, json_storage_result, lock_dirname):

    class JSONLocalStorageMock(JSONLocalStorage):
        stored_count = 0

        def save(self, *args, **kwargs):
            time.sleep(0.5)
            super().save(*args, **kwargs)
            JSONLocalStorageMock.stored_count += 1

    dirname = tmp_path / 'storage'
    dirname.mkdir()
    if lock_dirname:
        lock_dirname = tmp_path / lock_dirname
        lock_dirname.mkdir()

    expected_path = dirname / f'JSONLocalStorageMock_{base_encoded}' / key_encoded
    expected_lock_path = (lock_dirname or dirname) / f'{key_encoded}.lock'

    def _save_under_lock(storage, base_key, key, obj):
        with storage.lock(key) as lock:
            storage.save(base_key, {key: obj})
            with open(expected_path) as file:
                stored = json.load(file)
                check_stored_meta(stored['meta'])
                assert json_storage_result == stored
            assert os.path.exists(expected_lock_path), (expected_lock_path, os.listdir(os.path.dirname(expected_lock_path)))
            storage.cleanup(base_key, [key], lock)

    simultaneous_count = 10
    with futures.ThreadPoolExecutor(max_workers=simultaneous_count) as executor:
        tasks = []
        for _ in range(simultaneous_count):
            if lock_dirname:
                storage = JSONLocalStorageMock(dirname, locker=FileLocker(lock_dirname, 0))
            else:
                storage = JSONLocalStorageMock(dirname)
                storage.locker.timeout = 0
            tasks.append(executor.submit(_save_under_lock, storage, 'some_pipeline_key', 'some_key', obj_to_store))
            time.sleep(0.01)
        futures.wait(tasks)

    assert not os.path.exists(expected_lock_path), os.listdir(os.path.dirname(expected_lock_path))

    if tasks[0].exception():  # First tasks started when no lock was made.
        raise tasks[0].exception()

    exceptions = [task.exception() for task in tasks]
    assert simultaneous_count - 1 == sum(1 for task in tasks if task.exception()), exceptions
    assert 1 == JSONLocalStorageMock.stored_count, exceptions[0]


@pytest.mark.parametrize('lock_dirname', [None, 'lock_storage'])
def test_s3_storage(tmp_path, obj_to_store, base_encoded, key_encoded, json_storage_result, lock_dirname):

    @attr.s
    class S3ObjectMock:
        path: str = attr.ib()

        def delete(self):
            os.remove(self.path)

    @attr.s
    class StorageExceptionMock(Exception):
        response = attr.ib()

    @attr.s
    class BucketMock:
        dirname: str = attr.ib()

        def upload_fileobj(self, Fileobj: BytesIO, Key: str, *, ExtraArgs: Dict) -> None:
            with open(os.path.join(self.dirname, Key), 'wb') as file:
                Fileobj.seek(0)
                file.write(Fileobj.read())
                assert 'some_key' == ExtraArgs['Metadata']['key']
                assert json.loads(ExtraArgs['Metadata']['meta'])

        def download_fileobj(self, Key: str, Fileobj: BytesIO) -> None:
            try:
                with open(os.path.join(self.dirname, Key), 'rb') as file:
                    Fileobj.write(file.read())
            except FileNotFoundError:
                raise StorageExceptionMock({'Error': {'Code': '404', 'Message': 'Not Found'}})

        def Object(self, key: str) -> S3ObjectMock:
            return S3ObjectMock(os.path.join(self.dirname, key))

        @property
        def objects(self):
            return BucketObjectsCollectionMock(self)

    @attr.s
    class BucketObjectsCollectionMock:
        bucket: BucketMock = attr.ib()
        objs: List[S3ObjectMock] = attr.ib(factory=list)

        def filter(self, Prefix: str) -> 'BucketObjectsCollectionMock':
            return BucketObjectsCollectionMock(
                self.bucket,
                [
                    S3ObjectMock(os.path.join(self.bucket.dirname, name))
                    for name in os.listdir(self.bucket.dirname)
                    if name.startswith(Prefix)
                ]
            )

        def delete(self) -> None:
            for obj in self.objs:
                obj.delete()

    dirname = tmp_path / 'storage'
    dirname.mkdir()

    bucket = BucketMock(dirname)

    storage_kwargs = {}
    if lock_dirname:
        lock_dirname = tmp_path / lock_dirname
        lock_dirname.mkdir()
        storage_kwargs['locker'] = FileLocker(lock_dirname)

    storage = S3Storage(bucket, **storage_kwargs)

    with storage.lock('some_key') as lock:
        storage.save('some_pipeline_key', {'some_key': obj_to_store})

        with open(dirname / f'S3Storage_{base_encoded}_{key_encoded}', 'rb') as file:
            assert json_storage_result['value'].encode() == file.read()

        assert {'some_key': obj_to_store} == storage.load('some_pipeline_key', ['some_key'])

        if lock_dirname:
            assert os.path.exists(lock_dirname / f'{key_encoded}.lock')

        storage.cleanup('some_pipeline_key', ['some_key'], lock)

    assert not os.path.exists(dirname / f'S3Storage_{base_encoded}_{key_encoded}')
    if lock_dirname:
        assert not os.path.exists(lock_dirname / f'S3Storage_{key_encoded}.lock')
    assert not storage.load('some_pipeline_key', ['some_key'])


@pytest.mark.parametrize('start_after_iteration', [1, 2])
@pytest.mark.parametrize('overlap', [True, False])
def test_id_locks(tmp_path, start_after_iteration, overlap):
    process_period = 0.8
    process_duration = process_period / 2
    iterations = 4

    dirname = tmp_path / 'storage'
    dirname.mkdir()

    results = {'first': [], 'second': []}

    def run_process(name):
        locker = FileLocker(dirname)
        for iteration in range(1, 1 + iterations):
            print(f'Start process iteration: ({name}, {iteration})')
            try:
                with locker('some_key'):
                    print(f'Acquired lock by: {name}')
                    results[name].append({'locker._id': locker._id})
                    time.sleep(process_duration)
                print(f'Released lock from: {name}')
                time.sleep(process_period - process_duration)
            except Exception as exc:
                results[name].append(type(exc).__name__)

    simultaneous_count = 2
    with futures.ThreadPoolExecutor(max_workers=simultaneous_count) as executor:
        tasks = []
        tasks.append(executor.submit(run_process, 'first'))
        time.sleep(process_period * (start_after_iteration - 1) + process_duration * 0.5)
        if not overlap:
            time.sleep(process_duration * 0.6)
        tasks.append(executor.submit(run_process, 'second'))
        futures.wait(tasks)

    assert [{'locker._id': start_after_iteration}] * iterations == results['second'], results['second']
    assert (
        [{'locker._id': 0}] * start_after_iteration
        + ['NewerInstanceDetectedError'] * (iterations - start_after_iteration)
    ) == results['first'], results['first']
