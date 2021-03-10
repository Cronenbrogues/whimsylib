import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements/requirements-main.txt") as fh:
    requirements = fh.read().splitlines()

requirements = [f"{r.split('/')[-3]} @ {r}" for r in requirements]

setuptools.setup(
    name="whimsylib",
    version="0.1.2",
    author="The Arch Cronenbrogues",
    author_email="cronenbrogues@googlegroups.com",
    description="A generic game engine for text-based games, inspired by adventurelib.",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cronenbrogues/whimsylib",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
