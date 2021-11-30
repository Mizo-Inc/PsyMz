from setuptools import setup

setup(
    name='PsyMz',
    version='1.0.1',
    description='A simple python package for keeping Postgres connections alive indefinitely.',
    url='https://github.com/Mizo-Inc/psymz',
    author='John Ades',
    author_email='pizza@mizo.co',
    license='MIT',
    packages=['psymz'],
    install_requires=[
        'psycopg2',
    ],
    classifiers=[
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)