from setuptools import setup, find_packages

setup(
    name="disclog",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here
    author="Anshuman Dash",
    author_email="ansdash2@gmail.com",
    description="A tool for adding logging through discord.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Anshuman-UCSB/disclog",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
