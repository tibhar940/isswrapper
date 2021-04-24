import io
import os
import re
from distutils.core import setup

# get requirements to install
with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), "r") as fl:
    install_requires = fl.read().splitlines()

# get version
version_path = os.path.join(os.path.dirname(__file__), "isswrapper", "_version.py")
with io.open(version_path) as fl:
    version = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', fl.read(), re.M).group(1)

setup(
    name="isswrapper",
    version=version,
    author="Alexey Samoylov",
    description="Simple wrapper for Moscow Exchange API (ISS Queries)",
    long_description="Simple wrapper for Moscow Exchange API (ISS Queries)",
    url="https://github.com/tibhar940/isswrapper",
    packages=["isswrapper", "isswrapper/loaders"],
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires
)
