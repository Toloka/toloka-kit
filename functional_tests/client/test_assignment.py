from toloka.client.assignment import Assignment


def test_get_assignment(client):
    assignment = client.get_assignment('0001bbb562--617bfe98d17b912687d6d878')
    assert assignment.status == Assignment.Status.ACCEPTED


def test_get_assignments(client, pool_in_project_with_pool):
    assignments = list(client.get_assignments(pool_id=pool_in_project_with_pool.id, status=Assignment.Status.ACCEPTED))
    assert len(assignments) == 63


def test_get_assignments_df(client, pool_in_project_with_pool):
    assignments_df = client.get_assignments_df(
        pool_id=pool_in_project_with_pool.id
    )
    for column in ["INPUT:image", "OUTPUT:result", "GOLDEN:result"]:
        assert column in assignments_df.columns
    assert len(assignments_df) == 606
