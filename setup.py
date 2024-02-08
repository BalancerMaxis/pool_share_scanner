from setuptools import setup, find_packages

setup(
    name='pool_share_scanner',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'datetime',
        'gql',
        'requests_toolbelt'
    ],
    author='xeonus',
)
