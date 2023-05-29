from setuptools import find_packages, setup

requirements = [
    'pytest',
    'mock',
    'attrs',
]

setup(
    name='func_call_patcher',
    version='0.0.0',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)
