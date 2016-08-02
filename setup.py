from setuptools import setup, find_packages

setup(
    name='click-ioc',
    version='0.1',
    description='A simple implementation of a Python Click API with the IOC pattern.',
    author='Kevin Wu',
    author_email='contact@kevinwu.io',
    packages=find_packages(),

    install_requires=[
        'click',
    ],

    entry_points={
        'console_scripts': [
            'app = app:cli'
        ]
    }
)
