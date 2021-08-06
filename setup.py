from distutils.core import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="itscalledsoccer",
    version="0.0.1",
    description="Programmatically interact with the ASA API",
    long_description=long_description,
    author="American Soccer Analysis",
    author_email="americansocceranalysis@gmail.com",
    url="https://github.com/American-Soccer-Analysis/asa-package",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    keywords="stats soccer api american machine learning football",
)
