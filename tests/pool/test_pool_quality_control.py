import pytest

import toloka.client as client

from ..testutils.util_functions import check_headers


@pytest.fixture
def acceptance_rate_config_map():
    return {
        'collector_config': {'type': 'ACCEPTANCE_RATE'},
        'rules': [
            {
                'conditions': [
                    {'key': 'total_assignments_count', 'operator': 'GTE', 'value': 10},
                    {'key': 'rejected_assignments_rate', 'operator': 'GT', 'value': 0.12},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {
                        'scope': 'PROJECT',
                        'duration_days': 1,
                    }
                }
            }
        ]
    }


@pytest.fixture
def acceptance_rate_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.AcceptanceRate(),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[
                    client.conditions.TotalAssignmentsCount >= 10,
                    client.conditions.RejectedAssignmentsRate > 0.12,
                ],
                action=client.actions.Restriction(
                    scope=client.user_restriction.UserRestriction.PROJECT,
                    duration_days=1,
                ),
            )
        ]
    )


@pytest.fixture
def answer_count_config_map():
    return {
        'collector_config': {'type': 'ANSWER_COUNT'},
        'rules': [
            {
                'conditions': [
                    {'key': 'assignments_accepted_count', 'operator': 'GTE', 'value': 12},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {
                        'scope': 'POOL',
                        'duration_days': 2,
                        'private_comment': 'Completed 12 task suites in pool',
                    }
                }
            }
        ]
    }


@pytest.fixture
def answer_count_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.AnswerCount(),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[client.conditions.AssignmentsAcceptedCount >= 12],
                action=client.actions.Restriction(
                    scope=client.user_restriction.UserRestriction.POOL,
                    duration_days=2,
                    private_comment='Completed 12 task suites in pool',
                ),
            )
        ]
    )


@pytest.fixture
def assignments_assessment_config_map():
    return {
        'collector_config': {'type': 'ASSIGNMENTS_ASSESSMENT'},
        'rules': [
            {
                'conditions': [
                    {'key': 'rejected_assignments_count', 'operator': 'GTE', 'value': 2},
                    {'key': 'assessment_event', 'operator': 'EQ', 'value': 'REJECT'},
                ],
                'action': {
                    'type': 'CHANGE_OVERLAP',
                    'parameters': {
                        'delta': 1,
                        'open_pool': True,
                    }
                }
            },
            {
                'conditions': [
                    {'key': 'pending_assignments_count', 'operator': 'GT', 'value': 3},
                ],
                'action': {
                    'type': 'SET_SKILL',
                    'parameters': {
                        'skill_id': '2117',
                        'skill_value': 1,
                    }
                }
            }
        ]
    }


@pytest.fixture
def assignments_assessment_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.AssignmentsAssessment(),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[
                    client.conditions.RejectedAssignmentsCount >= 2,
                    client.conditions.AssessmentEvent == client.conditions.AssessmentEvent.REJECT,
                ],
                action=client.actions.ChangeOverlap(delta=1, open_pool=True),
            ),
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[client.conditions.PendingAssignmentsCount > 3],
                action=client.actions.SetSkill(skill_id='2117', skill_value=1),
            )
        ]
    )


@pytest.fixture
def assignment_submit_time_config_map():
    return {
        'collector_config': {
            'type': 'ASSIGNMENT_SUBMIT_TIME',
            'parameters': {'history_size': 10, 'fast_submit_threshold_seconds': 3},
        },
        'rules': [
            {
                'conditions': [
                    {'key': 'total_submitted_count', 'operator': 'EQ', 'value': 10},
                    {'key': 'fast_submitted_count', 'operator': 'GTE', 'value': 4},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {
                        'scope': 'PROJECT',
                        'duration_days': 1,
                        'private_comment': 'More than 4 fast answers',
                    }
                }
            }
        ]
    }


@pytest.fixture
def assignment_submit_time_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.AssignmentSubmitTime(
            history_size=10,
            fast_submit_threshold_seconds=3,
        ),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[
                    client.conditions.TotalSubmittedCount == 10,
                    client.conditions.FastSubmittedCount >= 4,
                ],
                action=client.actions.Restriction(
                    scope=client.user_restriction.UserRestriction.PROJECT,
                    duration_days=1,
                    private_comment='More than 4 fast answers',
                ),
            )
        ]
    )


@pytest.fixture
def captcha_config_map():
    return {
        'collector_config': {
            'type': 'CAPTCHA',
            'parameters': {'history_size': 10},
        },
        'rules': [
            {
                'conditions': [
                    {'key': 'stored_results_count', 'operator': 'EQ', 'value': 10},
                    {'key': 'success_rate', 'operator': 'LTE', 'value': 70.1},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {
                        'scope': 'PROJECT',
                        'duration_days': 2,
                        'private_comment': 'Incorrect captcha',
                    }
                }
            }
        ]
    }


@pytest.fixture
def captcha_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.Captcha(history_size=10),
        rules=[client.pool.QualityControl.QualityControlConfig.RuleConfig(
            conditions=[
                client.conditions.StoredResultsCount == 10,
                client.conditions.SuccessRate <= 70.1,
            ],
            action=client.actions.Restriction(
                scope=client.user_restriction.UserRestriction.Scope.PROJECT,
                duration_days=2,
                private_comment='Incorrect captcha',
            ),
        )]
    )


@pytest.fixture
def golden_set_config_map():
    return {
        'collector_config': {
            'type': 'GOLDEN_SET',
            'parameters': {'history_size': 10},
        },
        'rules': [
            {
                'conditions': [
                    {'key': 'total_answers_count', 'operator': 'GT', 'value': 7},
                ],
                'action': {
                    'type': 'SET_SKILL_FROM_OUTPUT_FIELD',
                    'parameters': {'skill_id': '42', 'from_field': 'correct_answers_rate'},
                }
            },
            {
                'conditions': [
                    {'key': 'total_answers_count', 'operator': 'GT', 'value': 7},
                    {'key': 'correct_answers_rate', 'operator': 'LT', 'value': 75.5},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {
                        'scope': 'PROJECT',
                        'duration_days': 1,
                        'private_comment': 'Failed to pass golden set',
                    },
                }
            }
        ]
    }


@pytest.fixture
def golden_set_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.GoldenSet(history_size=10),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[client.conditions.TotalAnswersCount > 7],
                action=client.actions.SetSkillFromOutputField(
                    skill_id='42',
                    from_field=client.conditions.RuleConditionKey.CORRECT_ANSWERS_RATE,
                ),
            ),
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[
                    client.conditions.TotalAnswersCount > 7,
                    client.conditions.CorrectAnswersRate < 75.5,
                ],
                action=client.actions.Restriction(
                    scope=client.user_restriction.UserRestriction.Scope.PROJECT,
                    duration_days=1,
                    private_comment='Failed to pass golden set',
                ),

            ),
        ]
    )


@pytest.fixture
def income_config_map():
    return {
        'collector_config': {'type': 'INCOME'},
        'rules': [
            {
                'conditions': [
                    {'key': 'income_sum_for_last_24_hours', 'operator': 'GTE', 'value': 20.0},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {'scope': 'ALL_PROJECTS', 'duration_days': 1}
                }
            }
        ]
    }


@pytest.fixture
def income_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.Income(),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[client.conditions.IncomeSumForLast24Hours >= 20.0],
                action=client.actions.Restriction(
                    scope=client.user_restriction.UserRestriction.ALL_PROJECTS,
                    duration_days=1,
                ),
            )
        ]
    )


@pytest.fixture
def majority_vote_config_map():
    return {
        'collector_config': {
            'type': 'MAJORITY_VOTE',
            'parameters': {
                'answer_threshold': 3,
                'history_size': 10
            },
        },
        'rules': [
            {
                'conditions': [
                    {'key': 'total_answers_count', 'operator': 'GT', 'value': 2},
                ],
                'action': {
                    'type': 'SET_SKILL_FROM_OUTPUT_FIELD',
                    'parameters': {
                        'skill_id': '43',
                        'from_field': 'incorrect_answers_rate',
                    }
                }
            }
        ]
    }


@pytest.fixture
def majority_vote_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.MajorityVote(answer_threshold=3, history_size=10),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[client.conditions.TotalAnswersCount > 2],
                action=client.actions.SetSkillFromOutputField(
                    skill_id='43',
                    from_field=client.conditions.RuleConditionKey.INCORRECT_ANSWERS_RATE,
                ),
            )
        ]
    )


@pytest.fixture
def skipped_in_row_assignment_config_map():
    return {
        'collector_config': {'type': 'SKIPPED_IN_ROW_ASSIGNMENTS'},
        'rules': [
            {
                'conditions': [
                    {'key': 'skipped_in_row_count', 'operator': 'GTE', 'value': 10},
                ],
                'action': {
                    'type': 'RESTRICTION',
                    'parameters': {
                        'scope': 'POOL',
                        'duration_days': 1,
                        'private_comment': 'Skipped more than 10 assignments',
                    }
                }
            }
        ]
    }


@pytest.fixture
def skipped_in_row_assignment_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.SkippedInRowAssignments(),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[client.conditions.SkippedInRowCount >= 10],
                action=client.actions.Restriction(
                    scope=client.user_restriction.UserRestriction.POOL,
                    duration_days=1,
                    private_comment='Skipped more than 10 assignments',
                ),
            )
        ]
    )


@pytest.fixture
def users_assessment_config_map():
    return {
        'collector_config': {'type': 'USERS_ASSESSMENT'},
        'rules': [
            {
                'conditions': [
                    {'key': 'pool_access_revoked_reason', 'operator': 'EQ', 'value': 'SKILL_CHANGE'},
                    {'key': 'skill_id', 'operator': 'EQ', 'value': '2626'},

                ],
                'action': {
                    'type': 'CHANGE_OVERLAP',
                    'parameters': {
                        'delta': 1,
                        'open_pool': True,
                    }
                }
            }
        ]
    }


@pytest.fixture
def users_assessment_config_object():
    return client.pool.QualityControl.QualityControlConfig(
        collector_config=client.collectors.UsersAssessment(),
        rules=[
            client.pool.QualityControl.QualityControlConfig.RuleConfig(
                conditions=[
                    client.conditions.PoolAccessRevokedReason == client.conditions.PoolAccessRevokedReason.SKILL_CHANGE,
                    client.conditions.SkillId == '2626',
                ],
                action=client.actions.ChangeOverlap(delta=1, open_pool=True),
            )
        ]
    )


@pytest.mark.parametrize(
    'collector_name',
    [
        'acceptance_rate',
        'answer_count',
        'assignments_assessment',
        'assignment_submit_time',
        'captcha',
        'income',
        'majority_vote',
        'golden_set',
        'skipped_in_row_assignment',
        'users_assessment',
    ],
)
def test_create_pool_with_collector(request, requests_mock, toloka_client, toloka_url, collector_name, pool_map_with_readonly):

    config_map = request.getfixturevalue(f'{collector_name}_config_map')
    config_object = request.getfixturevalue(f'{collector_name}_config_object')

    pool_map = {
        **pool_map_with_readonly,
        'quality_control': {
            'configs': [config_map],
            'captcha_frequency': 'MEDIUM',
            'training_requirement': {
                'training_pool_id': '21',
                'training_passing_skill_value': 85,
            },
        }
    }

    def pools(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_pool',
            'X-Low-Level-Method': 'create_pool',
        }
        check_headers(request, expected_headers)

        assert pool_map == request.json()
        return pool_map

    requests_mock.post(f'{toloka_url}/pools', json=pools, status_code=201)

    pool = client.structure(pool_map_with_readonly, client.pool.Pool)
    pool.quality_control = client.pool.QualityControl(
        configs=[config_object],
        captcha_frequency=client.pool.QualityControl.CaptchaFrequency.MEDIUM,
        training_requirement=client.pool.QualityControl.TrainingRequirement(
            training_pool_id='21',
            training_passing_skill_value=85,
        ),
    )

    result = toloka_client.create_pool(pool)
    assert pool_map == client.unstructure(result)
