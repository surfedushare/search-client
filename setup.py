import setuptools

from search_client.version import VERSION


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="search-client",
    version=VERSION,
    author="SURF",
    description="A Python wrapper around Open Search to make searching easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/surfedushare/search-client",
    packages=setuptools.find_packages(
        exclude=["tests*"]
    ),
    install_requires=[
        "Django>=4.2",
        "opensearch-py",
        "python-dateutil",
        "djangorestframework",
        "pytz",
        "requests-aws4auth",
    ],
    python_requires="~=3.10",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django :: 4.2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
