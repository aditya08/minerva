from setuptools import setup, find_packages

setup(name="Minerva",
        package_dir={"minerva":"src"},
        packages=["minerva"]
        package_data={"":["*.json"]})