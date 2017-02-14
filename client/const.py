# Constants

X = None  # To define center of mask

UNITS = {
    'unit': {
        'health': 0,
        'damage': [
            [1, 1, 1],
            [1, X, 1],
            [1, 1, 1]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'children': ['infantry', 'horseman']
    },
    'infantry': {
        'health': 0,
        'damage': [
            [1, 2, 1],
            [1, X, 1],
            [1, 1, 1]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 2, 0]
        ],
        'children': ['pikeman', 'archer', 'warrior']
    },
    'horseman': {
        'health': 0,
        'damage': [
            [2, 1, 2],
            [1, X, 1],
            [0, 1, 0]
        ],
        'support': [
            [0, 0, 0],
            [1, X, 1],
            [0, 0, 0]
        ],
        'children': ['dragoon', 'knight', 'hobbler']
    },
    'pikeman': {
        'health': 0,
        'damage': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
    },
    'archer': {
        'health': 0,
        'damage': [
            [1, 0, 1],
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
    },
    'warrior': {
        'health': 0,
        'damage': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
    },
    'dragoon': {
        'health': 0,
        'damage': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
    },
    'knight': {
        'health': 0,
        'damage': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
    },
    'hobbler': {
        'health': 0,
        'damage': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ],
        'support': [
            [0, 0, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
    }
}