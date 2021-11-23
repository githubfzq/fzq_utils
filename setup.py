from setuptools import setup, find_packages

required_packages = [
    "python-digitalocean",
    "configparser",
    "Pillow"
]

setup(
    name="fzq_utils",
    version="1.1",
    description="Personal utilities of FZQ.",
    author="fanzuquan",
    author_email="u201312526@alumni.hust.edu.cn",
    packages=find_packages(include='utils'),
    install_requires = required_packages,
    entry_points={"console_scripts": ["utils = utils.tools:main"]}
)