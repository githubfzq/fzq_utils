from setuptools import setup, find_packages

required_packages = [
    "python-digitalocean",
    "configparser"
]

setup(
    name="fzq_utils",
    version="1.0",
    description="Personal utilities of FZQ.",
    author="fanzuquan",
    author_email="u201312526@alumni.hust.edu.cn",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires = required_packages
)