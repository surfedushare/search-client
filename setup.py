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
        exclude=[
            "service", "service.*",
            "environments", "environments.*",
        ]
    ),
    install_requires=[
        "Django>=3.2",
        "opensearch-py",
        "python-dateutil",
        "djangorestframework",
        "pytz",
    ],
    python_requires="~=3.10",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Framework :: Django :: 3.2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
