from setuptools import setup

setup(
    name='templateer',
    version='1.0.0',
    py_modules=['templateer'],
    install_requires=[
        'Click',
        'Jinja2',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        templateer=templateer:generate
    ''',
)
