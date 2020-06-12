# Setup file needed for packaging

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metadata_mongo_ingester",
    version="1.1",
    author="Neil Kindlon",
    author_email="Neil.Kindlon@jax.org",
    description="Ingest metadata into mongodb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "jsonschema",
        "pymongo",
        "pytest",
    ],
    url="https://github.com/TheJacksonLaboratory/metadata_mongo_ingester", 
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
