from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="dabfs",
    author="Resul Tugay",
    author_email="resultugay@hotmail.com",
    url="https://github.com/resultugay/dabfs",
    license="MIT",
    version="0.1.5",
    packages=find_packages(),
    description="Dynamic BFS algorithm to compress graph",
    long_description=description,
    long_description_content_type="text/markdown",
)