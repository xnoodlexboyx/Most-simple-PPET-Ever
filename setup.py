from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ppet",
    version="0.1.0",
    author="xnoodlexboyx",
    author_email="TBD",
    description="A PUF Performance Evaluation Toolkit",
    long_description=open("proposal.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xnoodlexboyx/ppet",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: ParrotOS",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ppet=main:main',
        ],
    },
)