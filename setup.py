from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ppet",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A PUF Performance Evaluation Toolkit",
    long_description=open("proposal.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/ppet",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ppet=main:main',
        ],
    },
)