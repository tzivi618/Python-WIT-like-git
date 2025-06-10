from setuptools import setup

setup(
    name='finalProject',
    version='0.1',
    py_modules=['wit'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'init=wit:init',
            'add=wit:add',
            'commit=wit:commit',
            'log=wit:log',
            'status=wit:status',
            'checkout=wit:checkout',
        ],
    },
)
