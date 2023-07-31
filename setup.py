# setup.py

from setuptools import setup, find_packages

setup(
    name='sensor_config',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'ansible-runner' 
    ],
    entry_points={
        'console_scripts':
        'sensor_config = sensor_programmer:configure_sensor'
    }
)