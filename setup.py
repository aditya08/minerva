from setuptools import setup, find_packages

setup(name="Minerva",
        packages=find_packages(where='src'),
        package_dir={"":"src"},
        package_data={"":["*.json"]})