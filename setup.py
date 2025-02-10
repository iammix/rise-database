from setuptools import setup, find_packages

setup(
    name="rise-database",
    version="0.1.0",
    author="Konstantinos Mixios",
    author_email="k.mixios@gmail.com",
    description="A Python library for downloading, processing, and visualizing accelerometer RISE datasets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iammix/rise-database",  # Replace with your repo URL
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)