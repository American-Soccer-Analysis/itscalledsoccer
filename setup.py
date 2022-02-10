from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="itscalledsoccer",
    packages=find_packages(exclude=["tests", "tests.*"]),
    version="0.1.1",
    description="Programmatically interact with the American Soccer Analysis API",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author="American Soccer Analysis",
    author_email="americansocceranalysis@gmail.com",
    url="https://github.com/American-Soccer-Analysis/itscalledsoccer",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    keywords="stats soccer api american machine learning football",
)
