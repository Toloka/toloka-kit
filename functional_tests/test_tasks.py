import pytest
import datetime
from toloka.client.pool import Pool
from toloka.client.task import Task


@pytest.fixture(scope='session')
def pool(client, empty_project):
    new_pool = Pool(
        project_id=empty_project.id,
        private_name='Test pool',
        reward_per_assignment=0.01,
        assignment_max_duration_seconds=100,
        will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),
    )
    new_pool.set_mixer_config(real_tasks_count=1)
    new_pool = client.create_pool(new_pool)
    yield new_pool
    client.archive_pool(new_pool.id)
    assert client.get_pool(new_pool.id).status == Pool.Status.ARCHIVED


@pytest.fixture(scope='session')
def task(client, pool):
    new_task = Task(input_values={'url': 'https://toloka.yandex.com'}, pool_id=pool.id, overlap=1)
    new_task = client.create_task(new_task)
    return new_task


def test_pool_created(client, pool):
    retrieved_pool = client.get_pool(pool.id)
    assert retrieved_pool == pool
    assert retrieved_pool.status == Pool.Status.CLOSED


def test_task_created(client, task):
    retrieved_task = client.get_task(task.id)
    assert retrieved_task == task


def test_get_tasks(client, task):
    assert task == next(client.get_tasks(pool_id=task.pool_id, id_lte=task.id, id_gte=task.id))


def test_find_tasks(client, task):
    assert task == client.find_tasks(pool_id=task.pool_id, id_lte=task.id, id_gte=task.id).items[0]


@pytest.fixture
def task_with_patched_overlap(client, task):
    original_overlap = task.remaining_overlap
    patched_task = client.patch_task(task.id, overlap=10)
    yield patched_task
    client.patch_task(task.id, overlap=original_overlap)
    assert client.get_task(task.id).remaining_overlap == original_overlap


def test_patch_task(client, task_with_patched_overlap):
    assert client.get_task(task_with_patched_overlap.id) == task_with_patched_overlap
