import pytest

from MultiTerra import *

test_items = [
    [
        [1, 2, 3, 4],
        1,
        [
            [1, 2, 3, 4],
        ]
    ],
    [
        [1, 2, 3, 4],
        2,
        [
            [1, 3],
            [2, 4],
        ]
    ],
    [
        [1, 2, 3, 4],
        3,
        [
            [1, 4],
            [2],
            [3],
        ]
    ],
    [
        [1, 2, 3, 4],
        4,
        [
            [1],
            [2],
            [3],
            [4],
        ]
    ],
    [
        [1, 2, 3, 4],
        5,
        [
            [1],
            [2],
            [3],
            [4],
            [],
        ]
    ],
    [
        [1, 2, 3, 4],
        6,
        [
            [1],
            [2],
            [3],
            [4],
            [],
            [],
        ]
    ],
]


@pytest.fixture(params=test_items)
def next_item(request):
    return request.param


def test_dissect(next_item):
    t = MultiTerra()
    result = t._dissect(next_item[0], next_item[1])
    assert result == next_item[2]
