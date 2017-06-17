import itertools
import pytest
import main

# запуск тестів: py.test -v -s


def test_update():
    config = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
    }

    main.update(config, 'pylons', 7)
    assert config == {
        'ginger': {
            'django': 2,
            'flask': 3,
            'pylons': 1,
        },
        'cucumber': {
            'flask': 1,
            'pylons': 6,
        },
    } or config == {
        'ginger': {
            'django': 2,
            'flask': 3,
            'pylons': 2,
        },
        'cucumber': {
            'flask': 1,
            'pylons': 5,
        },
    }

    config = {
        'ginger1': {
            'django': 2,
        },
        'ginger2': {
            'flask': 5,
            'django': 3,
        },

        'ginger3': {
            'flask': 18,
            'django': 2,
        },
        'ginger4': {
            'flask': 5,
            'django': 3,
        },
    }
    main.update(config, 'pylons', 12)
    assert config == {
        'ginger1': {
            'django': 2,
            'pylons': 8
        },
        'ginger2': {
            'django': 3,
            'flask': 5,
            'pylons': 2
        },
        'ginger3': {
            'django': 2,
            'flask': 18
        },
        'ginger4': {
            'django': 3,
            'flask': 5,
            'pylons': 2
        }
    }


def test_initial():
    config = {
        'ginger': {},
        'cucumber': {},
    }

    main.update(config, 'flask', 3)
    main.update(config, 'django', 3)

    assert sum(config['ginger'].values()) == sum(config['cucumber'].values())
    assert sum(sum(x.values()) for x in config.values()) == 3+3


def test_predictable_config():
    services = [
        ('flask', 7),
        ('django', 13),
        ('pylons', 17)
    ]

    for permutation in itertools.permutations(services):
        config = {
            'ginger': {},
            'cucumber': {},
        }
        for svc, num in permutation:
            main.update(config, svc, num)
        assert sum(sum(x.values()) for x in config.values()) == 7+13+17